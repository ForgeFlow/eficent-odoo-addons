from odoo import _, api, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.constrains("timesheet_invoice_id", "journal_id")
    def _constrains_exclude_from_sale_order(self):
        if self.filtered(
            lambda line: line.timesheet_invoice_id and not line.journal_id
        ):
            labor_anal_journal = self.env["account.analytic.journal"].search(
                [("cost_type", "=", "labor")], limit=1
            )
            if not labor_anal_journal:
                raise ValidationError(
                    _("Please create an analytic journal for labor cost")
                )
