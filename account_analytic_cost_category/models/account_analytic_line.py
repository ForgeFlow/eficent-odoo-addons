# © 2014-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountAnalyticLine(models.Model):

    _inherit = "account.analytic.line"

    cost_category = fields.Selection(
        [("cogs", "Cost of Goods Sold"), ("expense", "Expense")],
        related="account_id.cost_category",
    )
