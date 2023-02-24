# Copyright 2017-23 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    date_start = fields.Date(string="Start Date")
    date = fields.Date(string="End Date")
