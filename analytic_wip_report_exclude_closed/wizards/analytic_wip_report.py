# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AnalyticWipReport(models.TransientModel):
    _inherit = 'analytic.wip.report'

    filter_project = fields.Boolean(
        'Filter By Project',
        default=True
    )
    only_closed = fields.Boolean(
        'Only Closed',
        default=False
    )

    @api.multi
    def analytic_wip_report_open_window(self):
        res = super(AnalyticWipReport, self).analytic_wip_report_open_window()
        res['domain'] = self._get_analytic_search_domain()
        return res

    @api.multi
    def _get_analytic_search_domain(self):
        comparing_date = self.fiscalyear_id.date_start
        start_date = '2100-12-31'
        if self.to_date:
            start_date = self.to_date
        stages = self.env['analytic.account.stage'].search(
            [('name', 'in', ('Closed', 'Cancelled'))]).ids

        if self.filter_project:
            if not self.only_closed:                
                domain = ['&', '|', ('stage_id', 'not in', stages),
                          '&',
                          ('stage_id', 'in', stages),
                          ('date', '>=', comparing_date),
                          ('date_start', '<=', start_date),
                          ('account_class', '=', 'project'),
                          ]
            else:
                domain = [('stage_id', 'in', stages),
                          ('date', '>=', comparing_date),
                          ('date_start', '<=', start_date),
                          ('account_class', '=', 'project'),
                          ]
        else:
            if not self.only_closed:
                domain = ['|', '&', ('date', '>=', comparing_date),
                          ('stage_id', 'in', stages),
                          ('stage_id', 'not in', stages)]
            else:
                domain = [('date', '>=', comparing_date),
                          ('stage_id', 'in', stages)]
        return domain
