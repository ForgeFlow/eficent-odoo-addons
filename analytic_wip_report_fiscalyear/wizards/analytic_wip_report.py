# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DT
from datetime import datetime


class AnalyticWipReport(models.TransientModel):

    _inherit = "analytic.wip.report"

    fiscalyear_id = fields.Many2one(
        "date.range",
        required=True,
        domain=[("type_id.name", "=", "Fiscal Year")],
    )
    from_date_fy = fields.Date("From (within the fiscal year)", required=True)
    to_date_fy = fields.Date("To (within the fiscal year)", required=True)

    @api.multi
    def analytic_wip_report_open_window(self):
        result_context = {}
        result = super(
            AnalyticWipReport, self
        ).analytic_wip_report_open_window()
        data = self.read()[0]
        if data["from_date"]:
            result_context.update(
                {"from_date": datetime.strftime(data["from_date"], DT)}
            )
        if data["to_date"]:
            result_context.update(
                {"to_date": datetime.strftime(data["to_date"], DT)}
            )
        if data["fiscalyear_id"]:
            result_context.update({"fiscalyear_id": data["fiscalyear_id"][0]})
        if data["from_date_fy"]:
            result_context.update(
                {"from_date_fy": datetime.strftime(data["from_date_fy"], DT)}
            )
        if data["to_date_fy"]:
            result_context.update(
                {"to_date_fy": datetime.strftime(data["to_date_fy"], DT)}
            )
        result["context"] = str(result_context)
        return result

    @api.onchange("fiscalyear_id")
    def onchange_fiscalyear_id(self):
        for rec in self:
            if rec.fiscalyear_id:
                rec.from_date_fy = rec.fiscalyear_id.date_start
                rec.to_date_fy = rec.fiscalyear_id.date_end
