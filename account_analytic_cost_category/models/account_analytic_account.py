# © 2014-17 ForgeFlow S.L.
# © 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountAnalyticAccount(models.Model):

    _inherit = "account.analytic.account"

    cost_category = fields.Selection(
        [("cogs", "Cost of Goods Sold"), ("expense", "Expense")],
        "Type of Cost",
        help="""Defines what type of cost does the analytic account carry
        from an employee perspective.""",
        default="expense",
    )
