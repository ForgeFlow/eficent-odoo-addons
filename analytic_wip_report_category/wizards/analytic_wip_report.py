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
        res = super(AnalyticWipReport, self)._get_analytic_search_domain()
        if self.category_id:
            res.append(('category_id', '=', self.category_id.id),)
        return res
