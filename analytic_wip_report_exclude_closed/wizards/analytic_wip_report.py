# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


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
    def _get_analytic_search_domain(self):
        comparing_date = self.from_date
        project_stage = self.env['analytic.account.stage'].\
            search([('name', 'in', ('Closed', 'Cancelled'))]).mapped('id') or []
        if self.filter_project and not comparing_date:
            project_ids = self.env['account.analytic.account'].\
                search([('account_class', '=', 'project'),
                        ('stage_id', 'not in', project_stage)])
            domain = [('id', 'in', project_ids.ids)] or []
        elif self.filter_project and comparing_date:
            project_ids = self.env['account.analytic.account'].\
                search([('date_start', '>=', comparing_date),
                        ('account_class', '=', 'project'),
                        ('stage_id', 'not in', project_stage)])
            domain = [('id', 'in', project_ids.ids)] or []
        elif not self.filter_project and comparing_date:
            project_ids = self.env['account.analytic.account'].\
                search([('date_start', '>=', comparing_date),
                        ('stage_id', 'not in', project_stage)])
            domain = [('id', 'in', project_ids.ids)] or []
        else:
            project_ids = self.env['account.analytic.account'].\
                search([('stage_id', 'not in', project_stage)])
            domain = [('id', 'in', project_ids.ids)] or []
        return domain
