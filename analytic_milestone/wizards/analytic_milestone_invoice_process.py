# Copyright 2017 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AnalyticMilestoneInvoiceProcess(models.TransientModel):
    _name = "analytic.milestone.invoice.process"
    _description = "Run Invoice Process Report"

    report_type = fields.Selection(
        [
            ('invoice', 'Existing Invoice'),
            ('milestone', 'Next Invoice Proposal')
        ],
        'Report Based on',
        default='invoice',
        required=True,
        help=' * The \'invoice\' report_type is to check what was invoice '
             'whereas the \'milestone\' report_type is used for to issue the'
             ' new invoice.'
    )

    @api.model
    def _get_invoice_domain(self):
        return [(
            'invoice_line_ids.milestone_id',
            'in', self.env.context.get('active_ids', []))]

    invoice_id = fields.Many2one('account.invoice',
                                 string='Invoices',
                                 domain=_get_invoice_domain)

    milestone_ids = fields.Many2many(
        comodel_name='analytic.milestone',
        string="Milestones to invoice")

    @api.model
    def default_get(self, fields):
        res = super(AnalyticMilestoneInvoiceProcess, self).default_get(fields)
        milestone_ids = self._context.get('active_ids', [])
        active_model = self._context.get('active_model')
        if not milestone_ids:
            return res
        assert active_model == 'analytic.milestone', \
            'Bad context propagation'
        items = [(4, x) for x in milestone_ids]
        res['milestone_ids'] = items
        res['invoice_id'] = self.env['analytic.milestone'].browse(
            milestone_ids).filtered(
            lambda m: m.invoice_line_ids).invoice_line_ids[0].invoice_id.id
        return res

    @api.multi
    def invoice_process_run(self):
        data = {'data': self.milestone_ids.ids,
                'invoice_id': self.invoice_id.id,
                'wizard': True,
                'report_type': self.report_type}
        return self.env.ref(
            "analytic_milestone.analytic_milestone_xlsx"
        ).report_action(self, data=data)
