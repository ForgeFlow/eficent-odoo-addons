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
    def _get_analytic_search_domain(self):
        comparing_date = self.from_date
        project_stage = self.env['project.project.stage'].\
            search([('name', 'ilike', 'Closed')]) or []
        if self.filter_project and self.filter_project is True \
                and comparing_date:
            project_ids = self.env['project.project'].\
                search([('date_start', '>=', comparing_date),
                        ('account_class', '=', 'project'),
                        ('stage_id', 'in', project_stage.ids)])
            domain = [('project_ids', 'in', project_ids.ids)] or []
        else:
            project_ids = self.env['project.project'].\
                search([('date_start', '>=', comparing_date),
                        ('stage_id', 'in', project_stage.ids)])
            domain = [('project_ids', 'in', project_ids.ids)] or []
        return domain

    @api.multi
    def analytic_wip_report_open_window(self):
        res = super(AnalyticWipReport, self).analytic_wip_report_open_window()
        ctx = safe_eval(res['context'])
        if not ctx.get('from_date', False):
            return res
        res['domain'] = self._get_analytic_search_domain()
        return res
