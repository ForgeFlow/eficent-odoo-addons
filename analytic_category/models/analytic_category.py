# Copyright 2018-19 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountAnalyticCategory(models.Model):
    _name = "account.analytic.category"
    _description = "Analytic Category"

    name = fields.Char("Name", required=True)
    code = fields.Char("Code")
