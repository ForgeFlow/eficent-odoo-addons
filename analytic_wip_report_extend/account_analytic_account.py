# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import decimal_precision as dp
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
            all_ids = self.get_child_accounts(cr, uid, [account.id],
                                              context=context).keys()
            query_params = [tuple(all_ids)]
            where_date = ''
            if context.get('from_date', False):
                where_date += " AND l.date >= %s"
                query_params += [context['from_date']]
            if context.get('to_date', False):
                where_date += " AND l.date <= %s"
                query_params += [context['to_date']]
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

            # Revenue adjustments entries
            cr.execute(
                """SELECT COALESCE(sum(amount),0.0)
                FROM account_analytic_line L
                INNER JOIN account_move_line AML
                ON L.move_id = AML.id
                INNER JOIN account_move AM
                ON AML.move_id = AM.id
                WHERE AM.category in ('close', 'open')
                AND L.account_id IN %s
                """ + where_date + """
                """, query_params)
            val = cr.fetchone()[0] or 0
            res[account.id]['under_over_adj'] = val
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
        'under_over_adj': fields.function(
            _wip_report, method=True, type='float', multi='wip_report',
            help="Revenue recognition adjustments"),
        }
