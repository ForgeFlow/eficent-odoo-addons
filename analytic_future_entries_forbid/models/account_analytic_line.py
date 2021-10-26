# Copyright 2021 ForgeFlow Sl.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, _
from odoo.exceptions import UserError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.multi
    @api.constrains('rule_ids')
    def _check_analytic_lock_date(self):
        for line in self:
            if self.journal_id.restrict_future_entries_posted:
                lock_to_date = tomorrow
            else:
                lock_to_date = False
            if lock_to_date and line.date >= lock_to_date:
                message = _("Future entries are not allowed."
                            "You can only enter entries for today or in the past")
                raise UserError(message)
