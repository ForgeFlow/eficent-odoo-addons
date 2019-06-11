# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AnalyticWipReport(models.TransientModel):
    _inherit = 'analytic.wip.report'

    category_id = fields.Many2one(
        "account.analytic.category", "Category", ondelete="restrict")

    @api.multi
    def _get_analytic_search_domain(self):
        comparing_date = self.fiscalyear_id.date_start
        start_date = '2100-12-31'
        if self.to_date:
            start_date = self.to_date
        stages = self.env['analytic.account.stage'].search(
            [('name', 'in', ('Closed', 'Cancelled'))]).ids

        if self.category_id:
            if not self.only_closed:
                domain = ['&', '|', ('stage_id', 'not in', stages),
                          '&',
                          ('stage_id', 'in', stages),
                          ('date', '>=', comparing_date),
                          ('date_start', '<=', start_date),
                          ('category_id', '=', self.category_id.id),
                          ('account_class', '=', 'project'),
                          ]
            else:
                domain = [('stage_id', 'in', stages),
                          ('date', '>=', comparing_date),
                          ('date_start', '<=', start_date),
                          ('category_id', '=', self.category_id.id),
                          ('account_class', '=', 'project'),
                          ]
            return domain
        else:
            return super(AnalyticWipReport, self)._get_analytic_search_domain()
