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

    @api.multi
    def analytic_wip_report_open_window(self):
        res = super(AnalyticWipReport, self).analytic_wip_report_open_window()
        res['domain'] = self._get_analytic_search_domain()
        return res

    @api.multi
    def _get_anal_domain(self):
        comparing_date = self.fiscalyear_id.date_start
        if self.filter_project and not comparing_date:
            domain = [('account_class', '=', 'project')]
        elif self.filter_project and comparing_date:
            domain = [('date', '>=', comparing_date),
                      ('account_class', '=', 'project')]
        elif not self.filter_project and comparing_date:
            domain = [('date', '>=', comparing_date)]
        else:
            domain = []
        return domain

    @api.multi
    def _get_analytic_search_domain(self):
        domain = self._get_anal_domain()
        project_ids = self.env['account.analytic.account'].search(
            domain, order='category_id, complete_wbs_code')
        domain = [('id', 'in', project_ids.ids), ] or []
        return domain
