# Copyright 2021 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo import _, api, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.constrains("date")
    def _check_lock_date(self):
        for line in self:
            if (
                not line.journal_id.restrict_lock_dates
                or line.account_id.surpass_lock_dates
            ):
                continue
            lock_date = line.journal_id.journal_lock_to_date
            if not lock_date:
                lock_date = datetime.now().date() + timedelta(days=1)
            else:
                lock_date = lock_date
            if lock_date and line.date >= lock_date:
                raise ValidationError(
                    _("You cannot add/modify entries after %s" % lock_date)
                )
        return True
