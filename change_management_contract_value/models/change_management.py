# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models, fields
from odoo.exceptions import ValidationError


class ChangeManagementChange(models.Model):
    _inherit = 'change.management.change'

    change_value = fields.Float(string='Value',
                                readonly=True,
                                help="Value of the Change",
                                states={'draft': [('readonly', False)]})
    analytic_line_plan_ids = fields.One2many(
        'account.analytic.line.plan',
        'change_id',
        string='Revenue planning lines',
        readonly=True,
    )
    change_template_id = fields.Many2one(
        'change.management.template',
        string='Change Template',
        readonly=True,
        states={'draft': [('readonly', False)]})

    @api.multi
    def copy(self, default=None):
        default = default or {}
        default.update({
            'analytic_line_plan_ids': []})
        return super(ChangeManagementChange, self).copy(default)

    @api.multi
    def _prepare_revenue_analytic_line_plan_ids(self):
        for change in self:
            plan_version_obj = self.env['account.analytic.plan.version']
            res = {}
            res['value'] = {}
            account_id = change.project_id.analytic_account_id
            if not change.change_template_id:
                raise ValidationError(_('Change template not found'))
            product_id = change.change_template_id.revenue_product_id
            journal_id = \
                product_id.revenue_analytic_plan_journal_id \
                and product_id.revenue_analytic_plan_journal_id.id \
                or False
            if not journal_id:
                raise ValidationError(
                    _('No revenue plan journal for the product'))
            version_id = change.change_template_id.version_id.id or False

            general_account_id = product_id.product_tmpl_id.\
                property_account_income_id.id
            if not general_account_id:
                general_account_id = product_id.categ_id.\
                    property_account_income_categ_id.id
            if not general_account_id:
                raise ValidationError(
                    _('There is no income account defined for this product: '
                      '"%s" (id:%d)') % (product_id.name,
                                         product_id.id,))
            default_plan = plan_version_obj.search(
                [('default_plan', '=', True)], limit=1)

            if account_id.active_analytic_planning_version != default_plan:
                raise ValidationError(
                    _('The active planning version of the analytic account '
                      'must be %s. ') % (default_plan.name,))

            return {
                'account_id': account_id.id,
                'name': product_id.name,
                'change_id': change.id,
                'ref': change.name,
                'date': change.date_approved,
                'product_id': product_id.id,
                'product_uom_id': product_id.uom_id.id,
                'unit_amount': 1,
                'amount': change.change_value,
                'general_account_id': general_account_id,
                'journal_id': journal_id,
                'version_id': version_id,
                'currency_id': account_id.company_id.currency_id.id,
                'amount_currency': change.change_value,
            }

    @api.multi
    def create_revenue_plan_lines(self):
        for change in self:
            res = []
            line_plan_obj = self.env['account.analytic.line.plan']
            line_vals = change._prepare_revenue_analytic_line_plan_ids()
            line_id = line_plan_obj.create(line_vals)
            res.append(line_id)
            return res

    @api.multi
    def set_state_accepted(self):
        res = super(ChangeManagementChange, self).set_state_accepted()
        self._delete_analytic_lines()
        for change in self:
            line_ids = []
            if not change.change_project_id:
                raise ValidationError(_('Change project not provided'))
            line_ids.extend(change.create_revenue_plan_lines())
        return res

    @api.multi
    def _delete_analytic_lines(self):
        for change in self:
            change.analytic_line_plan_ids.unlink()
        return True

    @api.multi
    def set_state_draft(self):
        res = super(ChangeManagementChange, self).set_state_draft()
        self._delete_analytic_lines()
        return res

    @api.multi
    def set_state_rejected(self):
        res = super(ChangeManagementChange, self).set_state_rejected()
        self._delete_analytic_lines()
        return res
