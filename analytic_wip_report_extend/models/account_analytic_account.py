# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import odoo.addons.decimal_precision as dp
from odoo import api, fields, models


class account_analytic_account(models.Model):

    _inherit = 'account.analytic.account'

    @api.multi
    def _compute_wip_report(self):
        res = super(account_analytic_account, self)._compute_wip_report()
        for account in self:
            # Estimated gross profit percentage
            try:
                res[account.id]['estimated_gross_profit_per'] = \
                    res[account.id]['estimated_gross_profit'] / \
                    res[account.id]['total_value'] * 100
            except ZeroDivisionError:
                res[account.id]['estimated_gross_profit_per'] = 0
            # Over/Under billings
            over_under_billings =\
                res[account.id]['under_billings'] - res[account.id
                                                        ]['over_billings']
            res[account.id]['under_over'] = over_under_billings
        return res

    estimated_gross_profit_per = fields.Float(
        compute='_compute_wip_report',
        string='Total Value',
        help="""Estimated gros profit percentage
             (estimated gross profit/total contract value)""",
        digits=dp.get_precision('Account')
    )
    under_over = fields.Float(
        compute='_compute_wip_report',
        help="""Total under/over (under_billed-over_billed)"""
    )
