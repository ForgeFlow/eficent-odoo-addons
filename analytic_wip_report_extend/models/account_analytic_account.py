# Copyright 2016 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import odoo.addons.decimal_precision as dp
from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):

    _inherit = "account.analytic.account"

    @api.multi
    def _compute_wip_report(self):
        res = super(AccountAnalyticAccount, self)._compute_wip_report()
        for account in self:
            # Estimated gross profit percentage
            try:
                account.estimated_gross_profit_per = (
                    account.estimated_gross_profit / account.total_value * 100
                )
            except ZeroDivisionError:
                account.estimated_gross_profit_per = 0
            # Over/Under billings
            over_under_billings = (
                account.under_billings - account.over_billings
            )
            account.under_over = over_under_billings
        return res

    estimated_gross_profit_per = fields.Float(
        compute="_compute_wip_report",
        string="Total Value (Percentage)",
        help="""Estimated gros profit percentage
             (estimated gross profit/total contract value)""",
        digits=dp.get_precision("Account"),
    )
    under_over = fields.Float(
        compute="_compute_wip_report",
        help="""Total under/over (under_billed-over_billed)""",
    )
