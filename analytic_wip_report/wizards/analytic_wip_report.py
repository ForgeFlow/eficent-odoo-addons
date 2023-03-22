# Copyright 2015 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AnalyticWipReport(models.TransientModel):
    _name = "analytic.wip.report"
    _description = "Work In Progress Statement Report"

    from_date = fields.Date("From")
    to_date = fields.Date("To")

    def analytic_wip_report_open_window(self):
        result_context = {}
        result = self.env.ref(
            "analytic_wip_report.action_account_analytic_account_wip_form"
        ).read()[0]
        data = self.read()[0]
        if data["from_date"]:
            result_context.update(
                {"from_date": data["from_date"].strftime(fields.DATE_FORMAT)}
            )
        if data["to_date"]:
            result_context.update(
                {"to_date": data["to_date"].strftime(fields.DATE_FORMAT)}
            )
        result["context"] = str(result_context)
        result["target"] = "main"
        return result
