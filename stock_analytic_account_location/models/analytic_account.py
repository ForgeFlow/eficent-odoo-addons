# Copyright 2017 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, models
from odoo.exceptions import ValidationError


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    @api.constrains("location_id")
    def _check_location(self):
        for analytic in self:
            if analytic.location_id:
                if analytic.location_id.analytic_account_id != analytic:
                    return ValidationError(
                        _(
                            """The location does not belong
                        to this project"""
                        )
                    )
        return True
