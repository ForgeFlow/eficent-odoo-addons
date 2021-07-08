from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    budget_hours = fields.Float(
        default=0,
        string="Budget Hours",
        help="Set manually the estimated hours for the project",
    )
    actual_hours = fields.Float(compute="_compute_actual_project_hours")

    @api.multi
    def _compute_actual_project_hours(self):
        analytic_line_obj = self.env["account.analytic.line"]
        # compute only sheet analytic lines
        for account in self:
            domain = [
                ("account_id", "child_of", account.ids),
                ("sheet_id", "!=", False),
            ]
            anal_groups = analytic_line_obj.read_group(
                domain, fields=["account_id", "unit_amount"], groupby=["account_id"],
            )
            actual_hours = sum(l["unit_amount"] for l in anal_groups)
            account.actual_hours = actual_hours
