# Copyright 2023 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    category_id = fields.Many2one(
        "account.analytic.category", "Category", ondelete="restrict"
    )
