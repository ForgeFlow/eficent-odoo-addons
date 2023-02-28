# Copyright 2021 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    surpass_lock_dates = fields.Boolean()

    def write(self, vals):
        # propagate surpass_lock_dates in the hierarchy
        if self and "surpass_lock_dates" in vals and not vals["surpass_lock_dates"]:
            self.mapped("child_ids").write({"surpass_lock_dates": False})
        elif self and "surpass_lock_dates" in vals and vals["surpass_lock_dates"]:
            self.mapped("child_ids").write({"surpass_lock_dates": True})
        return super(AccountAnalyticAccount, self).write(vals)
