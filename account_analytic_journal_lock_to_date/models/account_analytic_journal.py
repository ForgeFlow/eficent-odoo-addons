# Copyright 2021 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountAnalyticJournal(models.Model):
    _inherit = "account.analytic.journal"

    restrict_lock_dates = fields.Boolean()
    journal_lock_to_date = fields.Date(
        string="Lock to date",
        help="Moves cannot be entered nor modified in this "
        "journal prior to the lock to date, if empty tomorrow's date is considered",
    )
