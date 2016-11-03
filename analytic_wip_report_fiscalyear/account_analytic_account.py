# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import decimal_precision as dp
from openerp.osv import fields, orm
from openerp.tools.translate import _


class account_analytic_account(orm.Model):
    
    _inherit = 'account.analytic.account'

    def _wip_report_fy(self, cr, uid, ids, fields, arg, context=None):
        res = {}
        if context is None:
            context = {}

        for account in self.browse(cr, uid, ids, context=context):
            all_ids = self.get_child_accounts(cr, uid, [account.id], context=context).keys()

            res[account.id] = {'fy_revenue': 0,
                               'fy_costs': 0,
                               'fy_gross_profit': 0,
                               }

            query_params = [tuple(all_ids)]
            where_date = ''

            if context.get('from_date_fy', False):
                fromdate = context.get('from_date_fy')
            else:
                raise orm.except_orm(_('Error'),
                               _('The start date for the fiscal year has'
                                 ' not been provided.'))
            if context.get('from_date_fy', False):
                todate = context.get('to_date_fy')
            else:
                raise orm.except_orm(_('Error'),
                               _('The end date form the fiscal year has'
                                 ' not been provided.'))

            where_date += " AND l.date >= %s"
            query_params += [fromdate]

            where_date += " AND l.date <= %s"
            query_params += [todate]

            # Actual billings for the fiscal year
            cr.execute(
                """SELECT COALESCE(sum(amount),0.0)
                FROM account_analytic_line L
                INNER JOIN account_account AC
                ON L.general_account_id = AC.id
                INNER JOIN account_account_type AT
                ON AT.id = AC.user_type
                WHERE AT.report_type = 'income'
                AND L.account_id IN %s
                """ + where_date + """
                """, query_params)
            val = cr.fetchone()[0] or 0
            res[account.id]['fy_revenue'] = val

            # Actual costs for the fiscal year
            cr.execute(
                """SELECT COALESCE(-1*sum(amount),0.0)
                FROM account_analytic_line L
                INNER JOIN account_account AC
                ON L.general_account_id = AC.id
                INNER JOIN account_account_type AT
                ON AT.id = AC.user_type
                WHERE AT.report_type = 'expense'
                AND L.account_id IN %s
                """ + where_date + """
                """, query_params)
            val = cr.fetchone()[0] or 0
            res[account.id]['fy_costs'] = val

            # Gross margin
            res[account.id]['fy_gross_profit'] = \
                res[account.id]['fy_revenue'] - res[account.id]['fy_costs']

        return res

    _columns = {

        'fy_revenue': fields.function(
                _wip_report_fy, method=True, type='float',
                string='Fiscal Year Revenue',
                multi='wip_report_fy',
                help="Revenue for the provided Fiscal Year",
                digits_compute=dp.get_precision('Account')),

        'fy_costs': fields.function(
                _wip_report_fy, method=True, type='float',
                string='Fiscal Year Costs', multi='wip_report_fy',
                help="Costs for the provided Fiscal Year",
                digits_compute=dp.get_precision('Account')),

        'fy_gross_profit': fields.function(
                _wip_report_fy, method=True, type='float',
                string='Fiscal Year Gross Profit', multi='wip_report_fy',
                digits_compute=dp.get_precision('Account')),
        }
