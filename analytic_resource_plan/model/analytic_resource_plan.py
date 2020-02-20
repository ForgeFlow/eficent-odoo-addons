
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2018 Luxim d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import time
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AnalyticResourcePlanLine(models.Model):

    _name = 'analytic.resource.plan.line'
    _description = "Analytic Resource Planning lines"
    _inherit = 'mail.thread'

    @api.multi
    @api.depends('child_ids')
    def _compute_has_child(self):
        for line in self:
            line.has_child = False
            if line.child_ids:
                line.has_child = False
        return True

    account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Analytic Account',
        required=True,
        ondelete='cascade',
        index=True,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    name = fields.Char(
        string='Activity description',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    date = fields.Date(
        string='Date',
        required=True,
        index=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda *a: time.strftime('%Y-%m-%d')
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirm', 'Confirmed')
        ],
        string='Status',
        index=True,
        required=True,
        readonly=True,
        help=' * The \'Draft\' status is '
             'used when a user is encoding a new and '
             'unconfirmed resource plan line. \n* '
             'The \'Confirmed\' status is used for to confirm '
             'the execution of the resource plan lines.',
        default='draft'
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        readonly=True,
        required=True,
        states={'draft': [('readonly', False)]}
    )
    product_uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string='UoM',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    unit_amount = fields.Float(
        string='Planned unit_amount',
        readonly=True,
        required=True,
        states={'draft': [('readonly', False)]},
        help='Specifies the quantity that has '
             'been planned.',
        default=1
    )
    notes = fields.Text(
        string='Notes'
    )
    parent_id = fields.Many2one(
        'analytic.resource.plan.line',
        'Parent',
        readonly=True,
        ondelete='cascade'
    )
    child_ids = fields.One2many(
        comodel_name='analytic.resource.plan.line',
        inverse_name='parent_id',
        string='Child lines'
    )
    has_child = fields.Boolean(
        compute='_compute_has_child',
        string="Has child"
    )
    analytic_line_plan_ids = fields.One2many(
        comodel_name='account.analytic.line.plan',
        inverse_name='resource_plan_id',
        string='Planned costs',
        readonly=True
    )
    price_unit = fields.Float(
        string='Cost Price',
        groups='project.group_project_manager',
    )
    price_total = fields.Float(
        store=False,
        compute='_compute_get_price_total',
        string='Total Cost',
        groups='project.group_project_manager',
    )
    resource_type = fields.Selection(
        selection=[
            ('task', 'Task'), ('procurement', 'Procurement')
        ],
        string='Type',
        required=True,
        default='procurement'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Assign To',
        ondelete='set null'
    )

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        default['parent_id'] = False
        default['analytic_line_plan_ids'] = []
        res = super(AnalyticResourcePlanLine, self).copy(default)
        return res

    @api.model
    def _prepare_analytic_lines(self):
        plan_version_obj = self.env['account.analytic.plan.version']
        journal_id =\
            (self.product_id.expense_analytic_plan_journal_id and
             self.product_id.expense_analytic_plan_journal_id.id or False)
        general_account_id = (
            self.product_id.product_tmpl_id.property_account_expense_id.id
        )
        if not journal_id:
            raise ValidationError(_(
                'There is no analytic plan journal for product %s'
            ) % self.product_id.name)
        if not general_account_id:
            general_account_id = (
                self.product_id.categ_id.property_account_expense_categ_id.id
            )
        if not general_account_id:
            raise ValidationError(_(
                'There is no expense account defined '
                'for this product: "%s" (id:%d)'
            ) % (self.product_id.name, self.product_id.id,))
        default_plan = plan_version_obj.search(
            [('default_resource_plan', '=', True)],
            limit=1
        )

        if not default_plan:
            raise ValidationError(_('No active planning version for resource'
                                    ' plan exists.'))

        return [{
            'resource_plan_id': self.id,
            'account_id': self.account_id.id,
            'name': self.name,
            'date': self.date,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom_id.id,
            'unit_amount': self.unit_amount,
            'unit_price': self.price_unit,
            'amount': -1 * self.price_total,
            'general_account_id': general_account_id,
            'journal_id': journal_id,
            'notes': self.notes,
            'version_id': default_plan.id,
            'currency_id': self.account_id.company_id.currency_id.id,
        }]

    @api.model
    def _get_child_resource_plan_lines(self):
        result = {}
        curr_id = self.id
        result[curr_id] = True
        # Now add the children
        self.env.cr.execute('''
        WITH RECURSIVE children AS (
        SELECT parent_id, id
        FROM analytic_resource_plan_line
        WHERE parent_id = %s
        UNION ALL
        SELECT a.parent_id, a.id
        FROM analytic_resource_plan_line a
        JOIN children b ON(a.parent_id = b.id)
        )
        SELECT * FROM children order by parent_id
        ''', (curr_id,))
        res = self.env.cr.fetchall()
        for x, y in res:
            result[y] = True
        return result

    @api.model
    def create_analytic_lines(self):
        res = []
        line_plan_obj = self.env['account.analytic.line.plan']
        lines_vals = self._prepare_analytic_lines()
        for line_vals in lines_vals:
            line_plan_obj.create(line_vals)
        return res

    @api.model
    def _delete_analytic_lines(self):
        line_plan_obj = self.env['account.analytic.line.plan']
        ana_line = line_plan_obj.search([('resource_plan_id', '=', self.id)])
        ana_line.unlink()
        return True

    @api.multi
    def action_button_draft(self):
        for line in self:
            for child in line.child_ids:
                if child.state not in ('draft', 'plan'):
                    raise ValidationError(_('All the child resource plan '
                                            'lines must be in Draft state.'))
            line._delete_analytic_lines()
        return self.write({'state': 'draft'})

    @api.multi
    def action_button_confirm(self):
        for line in self:
            children = line._get_child_resource_plan_lines()
            for child in self.browse(children):
                if child.unit_amount == 0:
                    raise ValidationError(_('Quantity should be greater'
                                            ' than 0.'))
                if not child.child_ids:
                    child.create_analytic_lines()
                child.write({'state': 'confirm'})
        return True

    @api.onchange('product_id')
    def on_change_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            self.product_uom_id =\
                (self.product_id.uom_id and self.product_id.uom_id.id or False)
            self.price_unit = self.product_id.standard_price

    @api.multi
    def write(self, vals):
        analytic_obj = self.env['account.analytic.account']
        if 'account_id' in vals:
            analytic = analytic_obj.browse(vals['account_id'])
            if vals.get('date', False):
                vals['date'] = analytic.date
        return super(AnalyticResourcePlanLine, self).write(vals)

    @api.multi
    def unlink(self):
        for line in self:
            if line.analytic_line_plan_ids:
                raise ValidationError(
                    _('You cannot delete a record that refers to analytic plan'
                      ' lines'))
        return super(AnalyticResourcePlanLine, self).unlink()

    # PRICE DEFINITIONS
    @api.multi
    @api.depends('price_unit', 'unit_amount')
    def _compute_get_price_total(self):
        for resource in self:
            resource.price_total = resource.price_unit * resource.unit_amount

    @api.multi
    def _get_pricelist(self):
        self.ensure_one()
        partner_id = self._get_partner()
        if partner_id:
            if partner_id.property_product_pricelist:
                return partner_id.property_product_pricelist
        else:
            return False

    # RESOURCE TYPE
    @api.onchange('resource_type')
    def resource_type_change(self):
        if self.resource_type == 'procurement':
            self.user_id = False

    @api.multi
    @api.constrains('resource_type', 'product_uom_id')
    def _check_description(self):
        for resource in self:
            if resource.resource_type == 'task' and (
                resource.product_uom_id.category_id != (
                    resource.env.ref('product.uom_categ_wtime'))):
                raise ValidationError(_("When resource type is task, "
                                        "the uom category should be time"))

    @api.multi
    def action_open_view_rpl_form(self):
        self.with_context(view_buttons=True)
        view = {
            'name': _('Details'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'analytic.resource.plan.line',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': self.id,
            'context': self.env.context
        }
        return view
