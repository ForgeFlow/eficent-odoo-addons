# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    milestone_id = fields.Many2one(
        'analytic.milestone',
        string="Milestones"
    )


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def act_analytic_milestone(self):
        action = self.env.ref(
            'analytic_milestone.act_analytic_milestone').read()[0]

        mil = self.mapped('invoice_line_ids.milestone_id')
        if len(mil) > 1:
            action['domain'] = [('id', 'in', mil.ids)]
        elif mil:
            action['views'] = [(self.env.ref(
                'analytic_milestone.view_analytic_milestone_form').id, 'form')]
            action['res_id'] = mil.id
        return action
