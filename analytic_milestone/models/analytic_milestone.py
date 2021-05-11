# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from datetime import datetime
from odoo.tools import float_is_zero
from odoo.exceptions import ValidationError


class AnalyticMilestone(models.Model):
    _name = 'analytic.milestone'
    _description = 'Milestone'
    _order = 'sequence asc, milestone_date desc'

    sequence = fields.Char("Item No.")
    name = fields.Char(
        string='Description',
        required=True
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
        help='Milestone approved',
        default='draft'
    )
    percent = fields.Float("Milestone Percent %")
    milestone_date = fields.Date(
        string='Milestone Date',
        required=True,
        index=True,
    )
    approval_date = fields.Date(
        string='Approval Date',
        readonly=True
    )
    invoice_date = fields.Date(
        string='Invoice Date',
        compute='compute_invoice_date'
    )
    base_amount = fields.Float(
        string='Base Contract Amount',
        required=True,
        deafult=0.0
    )
    invoice_amount = fields.Float(
        string='Invoice Amount',
        compute='compute_invoice_amount'
    )
    previous_amount = fields.Float(
        string='Previous Invoice Amount',
        compute='compute_previous_invoice_amount'
    )
    next_amount = fields.Float(
        string='This invoice amount',
        compute='compute_next_amount'
    )
    account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Analytic Account',
        required=True,
        ondelete='restrict',
        index=True
    )

    project_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Root Analytic Account',
        related='account_id.project_analytic_id',
        store=True,
        index=True
    )
    invoice_line_ids = fields.One2many(
        comodel_name='account.invoice.line', inverse_name="milestone_id",
        string='Invoice Lines')
    amount_residual = fields.Float(
        string='Due Amount',
        compute='compute_amount_residual'
    )
    invoice_count = fields.Integer(string='# of Invoices',
                                   compute='compute_invoice_count',
                                   readonly=True)
    partner_id = fields.Many2one(related='account_id.partner_id')

    def check_bounds(self):
        if len(self.mapped('project_analytic_id')) != 1:
            raise ValidationError(
                _("Please select only one project"))
        return True

    @api.multi
    def compute_amount_residual(self):
        for rec in self:
            rec.amount_residual = \
                sum(rec.invoice_line_ids.mapped('invoice_id.residual')) or 0.0

    @api.depends('invoice_line_ids')
    def compute_invoice_count(self):
        for rec in self:
            invoices = rec.mapped(
                'invoice_line_ids.invoice_id'
            )
            rec.invoice_count = len(invoices)

    @api.onchange('account_id')
    def onchange_account_id(self):
        if not self.partner_id.id:
            self.partner_id = self.account_id.partner_id

    @api.multi
    def _compute_partner_id(self):
        for rec in self:
            rec.partner_id = rec.account_id.partner_id

    @api.multi
    def compute_invoice_date(self):
        for rec in self:
            if not rec.invoice_line_ids:
                rec.invoice_date = rec.milestone_date
            else:
                lines = rec.invoice_line_ids.sorted(
                    lambda il: il.invoice_id.date_invoice)
                # lines sorted to older to new, take the last
                rec.invoice_date = lines[-1].invoice_id.date_invoice

    @api.multi
    def compute_previous_invoice_amount(self):
        for rec in self:
            rec.previous_amount = \
                sum(rec.invoice_line_ids.mapped('price_subtotal')) or 0.0

    @api.multi
    def compute_invoice_amount(self):
        for rec in self:
            rec.invoice_amount = rec.base_amount * (rec.percent / 100.0)

    @api.multi
    def compute_next_amount(self):
        for rec in self:
            if rec.state == 'draft':
                rec.ext_amount = 0.0
            else:
                rec.next_amount = rec.invoice_amount - rec.previous_amount

    @api.multi
    def action_button_draft(self):
        return self.write({'state': 'draft',
                           'approval_date': False})

    @api.multi
    def action_button_confirm(self):
        return self.write({'state': 'confirm',
                           'approval_date': datetime.now()})

    @api.multi
    def _prepare_invoice_line(self, qty, partner=False, account=False):
        """
        Prepare the dict of values to create the new invoice line for a billing
        plan.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        if not account:
            account = (self.account_id.milestone_product_id.
                       property_account_income_id or
                       self.account_id.milestone_product_id.categ_id.
                       property_account_income_categ_id)
        if not account:
            raise ValidationError(
                _('Please define income account for this product: "%s" (id:%d)'
                  ' - or for its category: "%s".') %
                (self.account_id.milestone_product_id.name,
                 self.account_id.milestone_product_id.id,
                 self.account_id.milestone_product_id.categ_id.name))
        if not partner:
            partner = self.account_id.partner_id
        if not partner:
            raise ValidationError("No partner specified")
        fpos = partner.property_account_position_id
        if fpos:
            account = fpos.map_account(account)
            taxes = fpos.map_tax(
                self.account_id.milestone_product_id.taxes_id, partner=partner)
        if qty == 0.0:
            raise ValidationError("Cannot invoice zero qty")
        res = {
            'name': self.display_name,
            'origin': self.display_name,
            'account_id': account.id,
            'price_unit': self.next_amount / qty,
            'quantity': qty,
            'uom_id': self.account_id.milestone_product_id.uom_id.id or False,
            'product_id': self.account_id.milestone_product_id.id or False,
            'invoice_line_tax_ids': [(6, 0, taxes.ids)] if fpos else False,
            'account_analytic_id': self.account_id.id,
            'milestone_id': self.id,
        }
        return res

    @api.multi
    def action_open_view_milestone_form(self):
        self.with_context(view_buttons=True)
        view = self.env.ref('analytic_milestone.view_analytic_milestone_form')
        view = {
            'name': _('Details'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'analytic.milestone',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': self.id,
            'context': self.env.context
        }
        return view

    @api.multi
    def invoice_line_create(self, invoice_id, qty, partner=False,
                            account=False):
        """ Create an invoice line.
            :param invoice_id: integer
            :param qty: float quantity to invoice
            :param partner: partner invoice
            :param account: account in invoice line
            :returns recordset of account.invoice.line created
        """
        invoice_lines = self.env['account.invoice.line']
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for plan in self:
            if not float_is_zero(qty, precision_digits=precision):
                vals = plan._prepare_invoice_line(qty=qty, partner=partner,
                                                  account=account)
                vals.update({
                    'invoice_id': invoice_id,
                })
                invoice_lines |= self.env['account.invoice.line'].create(vals)
        return invoice_lines

    @api.multi
    def _prepare_invoice(self, partner_id):
        """
        Prepare the dict of values to create the new invoice for a plan.
        """
        self.ensure_one()
        journal_id = (
            self.env['account.invoice'].default_get(['journal_id'])
            ['journal_id'])
        if not journal_id:
            raise ValidationError(_(
                'Please define an accounting sales journal for this company.'))
        invoice_vals = {
            'name': self.name or '',
            'origin': self.name,
            'date_invoice': self.invoice_date,
            'type': 'out_invoice',
            'account_id': partner_id.property_account_receivable_id.id,
            'partner_id': partner_id.id,
            'journal_id': journal_id,
            'currency_id':
                partner_id.property_product_pricelist.currency_id.id,
            'payment_term_id': partner_id.property_payment_term_id.id,
            'fiscal_position_id':
                partner_id.property_account_position_id.id,
            'user_id': partner_id.user_id.id or self.env.uid,
        }
        return invoice_vals

    @api.multi
    def action_view_invoice(self):
        invoices = self.mapped('invoice_line_ids.invoice_id')
        action = self.env.ref('account.action_invoice_tree1').read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            action['views'] = [
                (self.env.ref('account.invoice_form').id, 'form')]
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
