# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv


class account_analytic_account(osv.osv):
    
    _inherit = 'account.analytic.account'

    def _wip_report(self, cr, uid, ids, fields, arg, context=None):
        res = super(account_analytic_account, self)._wip_report(cr, uid,
                                                                ids, fields,
                                                                arg,
                                                                context)
        if context is None:
            context = {}

        for account in self.browse(cr, uid, ids, context=context):
            # Estimated gross profit percentage
            try:
                res[account.id]['estimated_gross_profit_per'] = \
                    res[account.id]['estimated_gross_profit'] / \
                    res[account.id]['total_value'] * 100
            except ZeroDivisionError:
                res[account.id]['estimated_gross_profit_per'] = 0
            # Over/Under billings
            over_under_billings = res[account.id]['under_billings'] - \
                                  res[account.id]['over_billings']
            res[account.id]['under_over'] = over_under_billings
        return res

    _columns = {
        'estimated_gross_profit_per': fields.function(
            _wip_report, method=True, type='float', string='Total Value',
            multi='wip_report',
            help="Estimated gros profit percentage (estimated gross profit/"
                 "total contract value)",
            digits_compute=dp.get_precision('Account')),

        'under_over': fields.function(
            _wip_report, method=True, type='float', multi='wip_report',
            help="Total under/over (under_billed-over_billed)"),
        }
