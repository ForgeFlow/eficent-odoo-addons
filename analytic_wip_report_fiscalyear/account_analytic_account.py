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
from dateutil.relativedelta import relativedelta
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DT


class account_analytic_account(orm.Model):
    
    _inherit = 'account.analytic.account'

    def _wip_report_fy(self, cr, uid, ids, fields, arg, context=None):
        res = self._wip_report(cr, uid, ids, fields, arg, context)
        if context is None:
            context = {}

        for account in self.browse(cr, uid, ids, context=context):
            all_ids = self.get_child_accounts(cr, uid, [account.id], context=context).keys()

            res[account.id].update(
                {'fy_billings': 0,
                 'fy_costs': 0,
                 'fy_gross_profit': 0,
                 'fy_actual_costs': 0,
                 'fy_actual_material_cost': 0,
                 'fy_actual_labor_cost': 0,
                 'actual_costs_fy': 0,
                 'percent_complete_fy': 0,
                 'total_estimated_costs_fy': 0,
                 'earned_revenue_fy': 0,
                 'total_value_fy': 0,
                 'total_value_end_fy': 0,
                 'earned_revenue_end_fy': 0
                 })

            query_params = [tuple(all_ids)]
            query_params_fy = [tuple(all_ids)]
            query_params_fy_end = [tuple(all_ids)]
            where_date = ''
            where_date_fy = ''
            where_date_fy_end = ''

            if context.get('from_date_fy', False):
                fromdate = context.get('from_date_fy')
                fromdatefy = datetime.strptime(
                    fromdate, DT) - relativedelta(days=1)
                fromdatefy = datetime.strftime(fromdatefy, DT)
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

            where_date_fy += " AND l.date <= %s"
            where_date_fy_end += " AND l.date <= %s"
            query_params_fy += [fromdatefy]
            query_params_fy_end += [todate]

            # Actual billings for the fiscal year
            cr.execute(
                """SELECT amount, L.id
                FROM account_analytic_line L
                INNER JOIN account_account AC
                ON L.general_account_id = AC.id
                INNER JOIN account_account_type AT
                ON AT.id = AC.user_type
                WHERE AT.report_type = 'income'
                AND L.account_id IN %s
                """ + where_date + """
                """, query_params)
            res[account.id]['fy_billings_line_ids'] = []
            for (val, line_id) in cr.fetchall():
                res[account.id]['fy_billings'] += val
                res[account.id]['fy_billings_line_ids'].append(line_id)

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

            # Revenue at the end of the last year to get the revenue of this
            # year

            # Total Value beginning year
            cr.execute(
                """SELECT COALESCE(sum(amount),0.0) AS total_value
                FROM account_analytic_line_plan AS L
                LEFT JOIN account_analytic_account AS A
                ON L.account_id = A.id
                INNER JOIN account_account AC
                ON L.general_account_id = AC.id
                INNER JOIN account_account_type AT
                ON AT.id = AC.user_type
                WHERE AT.report_type = 'income'
                AND l.account_id IN %s
                AND a.active_analytic_planning_version = l.version_id
                """ + where_date_fy + """
                """,
                query_params_fy)
            val = cr.fetchone()[0] or 0
            res[account.id]['total_value_fy'] = val

            # Total Value end year
            cr.execute(
                """SELECT COALESCE(sum(amount),0.0) AS total_value
                FROM account_analytic_line_plan AS L
                LEFT JOIN account_analytic_account AS A
                ON L.account_id = A.id
                INNER JOIN account_account AC
                ON L.general_account_id = AC.id
                INNER JOIN account_account_type AT
                ON AT.id = AC.user_type
                WHERE AT.report_type = 'income'
                AND l.account_id IN %s
                AND a.active_analytic_planning_version = l.version_id
                """ + where_date_fy_end + """
                """,
                query_params_fy_end)
            val = cr.fetchone()[0] or 0
            res[account.id]['total_value_end_fy'] = val

            cr.execute(
                """
                SELECT COALESCE(-1*sum(amount),0.0) total
                                FROM account_analytic_line L
                                INNER JOIN account_analytic_journal AAJ
                                ON AAJ.id = L.journal_id
                                INNER JOIN account_account AC
                                ON L.general_account_id = AC.id
                                INNER JOIN account_account_type AT
                                ON AT.id = AC.user_type
                                WHERE AT.report_type = 'expense'
                                AND L.account_id in %s
                """ + where_date_fy + """
                """, query_params_fy)
            res[account.id]['actual_costs_fy'] = 0
            val = cr.fetchone()[0] or 0
            res[account.id]['actual_costs_fy'] += val

            cr.execute(
                """
                SELECT COALESCE(-1*sum(amount),0.0) total
                                FROM account_analytic_line L
                                INNER JOIN account_analytic_journal AAJ
                                ON AAJ.id = L.journal_id
                                INNER JOIN account_account AC
                                ON L.general_account_id = AC.id
                                INNER JOIN account_account_type AT
                                ON AT.id = AC.user_type
                                WHERE AT.report_type = 'expense'
                                AND L.account_id in %s
                """ + where_date_fy_end + """
                """,
                query_params_fy_end)
            res[account.id]['actual_costs_end_fy'] = 0
            val = cr.fetchone()[0] or 0
            res[account.id]['actual_costs_end_fy'] += val

            # Total estimated costs at the beggining of the fiscal year
            cr.execute("""
            SELECT COALESCE(-1*sum(amount),0.0) AS total_value
            FROM account_analytic_line_plan AS L
            LEFT JOIN account_analytic_account AS A
            ON L.account_id = A.id
            INNER JOIN account_account AC
            ON L.general_account_id = AC.id
            INNER JOIN account_account_type AT
            ON AT.id = AC.user_type
            WHERE AT.report_type = 'expense'
            AND L.account_id IN %s
            AND A.active_analytic_planning_version = L.version_id
            """ + where_date_fy + """
            """, query_params_fy)
            val = cr.fetchone()[0] or 0
            res[account.id]['total_estimated_costs_fy'] = val

            # Total estimated costs at the end of the fiscal year
            cr.execute("""
            SELECT COALESCE(-1*sum(amount),0.0) AS total_value
            FROM account_analytic_line_plan AS L
            LEFT JOIN account_analytic_account AS A
            ON L.account_id = A.id
            INNER JOIN account_account AC
            ON L.general_account_id = AC.id
            INNER JOIN account_account_type AT
            ON AT.id = AC.user_type
            WHERE AT.report_type = 'expense'
            AND L.account_id IN %s
            AND A.active_analytic_planning_version = L.version_id
            """ + where_date_fy_end + """
            """, query_params_fy_end)
            val = cr.fetchone()[0] or 0
            res[account.id]['total_estimated_costs_end_fy'] = val

            try:
                res[account.id]['percent_complete_fy'] = \
                    (res[account.id]['actual_costs_fy'] / res[account.id]['total_estimated_costs_fy']) * 100
            except ZeroDivisionError:
                res[account.id]['percent_complete_fy'] = 0

            try:
                res[account.id]['percent_complete_end_fy'] = \
                    (res[account.id]['actual_costs_end_fy'] / res[account.id]['total_estimated_costs_end_fy']) * 100
            except ZeroDivisionError:
                res[account.id]['percent_complete_end_fy'] = 0

            # Earned revenue at beginning of the year
            res[account.id]['earned_revenue_fy'] = \
                res[account.id]['percent_complete_fy']/100 * res[account.id]['total_value_fy']
            # Earned revenue at end of the year
            res[account.id]['earned_revenue_end_fy'] = \
                res[account.id]['percent_complete_end_fy']/100 * res[account.id]['total_value_end_fy']
            # Earned revenue at current year
            res[account.id]['fy_revenue2'] = res[account.id]['earned_revenue_end_fy'] - res[account.id]['earned_revenue_fy']
            # Earned revenue based on billings
            res[account.id]['fy_revenue'] = res[account.id]['fy_billings'] + res[account.id]['under_billings'] - res[account.id]['over_billings']
            # Gross margin
            res[account.id]['fy_gross_profit'] = \
                res[account.id]['fy_revenue2'] - res[account.id]['fy_costs']

            # Actual costs to date
            cr.execute(
                """
                SELECT amount, L.id, AAJ.cost_type
                                FROM account_analytic_line L
                                INNER JOIN account_analytic_journal AAJ
                                ON AAJ.id = L.journal_id
                                INNER JOIN account_account AC
                                ON L.general_account_id = AC.id
                                INNER JOIN account_account_type AT
                                ON AT.id = AC.user_type
                                WHERE AT.report_type = 'expense'
                                AND L.account_id in %s
                """ + where_date + """
                """, query_params)
            res[account.id]['fy_actual_costs'] = 0
            res[account.id]['fy_actual_cost_line_ids'] = []
            res[account.id]['fy_actual_material_line_ids'] = []
            res[account.id]['fy_actual_labor_line_ids'] = []
            for (total, line_id, cost_type) in cr.fetchall():
                if cost_type in ('material', 'revenue'):
                    res[account.id]['fy_actual_material_cost'] -=total
                    res[account.id]['fy_actual_material_line_ids'].append(line_id)
                elif cost_type == 'labor':
                    res[account.id]['fy_actual_labor_cost'] -= total
                    res[account.id]['fy_actual_labor_line_ids'].append(line_id)
                res[account.id]['fy_actual_costs'] -= total
                res[account.id]['fy_actual_cost_line_ids'].append(line_id)

        return res

    _columns = {
        'total_value_fy': fields.function(
            _wip_report_fy, method=True, type='float', string='Total Value prior FY',
            multi='wip_report',
            help="Total estimated (prior year) value of the contract",
            digits_compute=dp.get_precision('Account')),
        'total_value_end_fy': fields.function(
            _wip_report_fy, method=True, type='float',
            string='Total Value end FY',
            multi='wip_report',
            help="Total estimated (end year) value of the contract",
            digits_compute=dp.get_precision('Account')),
        'fy_revenue': fields.function(
            _wip_report_fy, method=True, type='float',
            string='FY Revenue based on billings',
            multi='wip_report_fy',
            help="""Revenue for the provided Fiscal Year. This calculated
             by adding the billings for the fiscal year and the under/over 
             billed for the contract. Thus, it will include the billings in 
             excess of cost (under billed) and the costs in excess 
             of billings (over billed).""",
            digits_compute=dp.get_precision('Account')),
        'fy_revenue2': fields.function(
            _wip_report_fy, method=True, type='float',
            string='FY Revenue based on prior year',
            multi='wip_report_fy',
            help="""Revenue earned to date (current schedule) MINUS Revenue
             earned to date (prior year) = Revenue Earned (current period)""",
            digits_compute=dp.get_precision('Account')),
        'earned_revenue_fy': fields.function(
            _wip_report_fy, method=True, type='float',
            string='Revenue at beginning of the year',
            multi='wip_report_fy',
            digits_compute=dp.get_precision('Account')),
        'earned_revenue_end_fy': fields.function(
            _wip_report_fy, method=True, type='float',
            string='Revenue at end of the year',
            multi='wip_report_fy',
            digits_compute=dp.get_precision('Account')),
        'fy_billings': fields.function(
                _wip_report_fy, method=True, type='float',
                string='Fiscal Year Billings',
                multi='wip_report_fy',
                help="Billings for the provided Fiscal Year",
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
        'fy_actual_costs': fields.function(
            _wip_report_fy, method=True, type='float',
            string='Fiscal Year Actual Costs', multi='wip_report_fy',
            digits_compute=dp.get_precision('Account')),
        'actual_costs_fy': fields.function(
            _wip_report_fy, method=True, type='float',
            string='Last Year actual cost', multi='wip_report_fy',
            digits_compute=dp.get_precision('Account')),
        'actual_costs_end_fy': fields.function(
            _wip_report_fy, method=True, type='float',
            string='End fiscal Year actual cost', multi='wip_report_fy',
            digits_compute=dp.get_precision('Account')),
        'total_estimated_costs_fy': fields.function(
            _wip_report_fy, method=True, type='float',
            string='Estimated cost beginning of year', multi='wip_report_fy',
            digits_compute=dp.get_precision('Account')),
        'total_estimated_costs_end_fy': fields.function(
            _wip_report_fy, method=True, type='float',
            string='Estimated cost end fiscal year', multi='wip_report_fy',
            digits_compute=dp.get_precision('Account')),
        'percent_complete_fy': fields.function(
            _wip_report_fy, method=True, type='float',
            string='Percent Complete beginning fy',
            multi='wip_report', digits_compute=dp.get_precision('Account')),
        'percent_complete_end_fy': fields.function(
            _wip_report_fy, method=True, type='float',
            string='Percent Complete end fy',
            multi='wip_report', digits_compute=dp.get_precision('Account')),
        'fy_actual_material_cost': fields.function(
            _wip_report_fy, method=True, type='float',
            string='Fiscal Year Material Costs', multi='wip_report_fy',
            digits_compute=dp.get_precision('Account')),

        'fy_actual_labor_cost': fields.function(
            _wip_report_fy, method=True, type='float',
            string='Fiscal Year Labor Costs', multi='wip_report_fy',
            digits_compute=dp.get_precision('Account')),
        'fy_actual_cost_line_ids': fields.function(
            _wip_report_fy, method=True, type='many2many',
            relation="account.analytic.line", string="Detail",
            multi='wip_report'),
        'fy_actual_labor_line_ids': fields.function(
            _wip_report_fy, method=True, type='many2many',
            relation="account.analytic.line", string="Detail",
            multi='wip_report'),
        'fy_actual_material_line_ids': fields.function(
            _wip_report_fy, method=True, type='many2many',
            relation="account.analytic.line", string="Detail",
            multi='wip_report'),
        'fy_billings_line_ids': fields.function(
            _wip_report_fy, method=True, type='many2many',
            relation="account.analytic.line", string="Detail",
            multi='wip_report'),
        }


    def action_open_fy_cost_lines(self, cr, uid, ids, context=None):
        """
        :return dict: dictionary value for created view
        """
        if context is None:
            context = {}
        line = self.browse(cr, uid, ids[0], context)
        bill_lines = [x.id for x in line.fy_actual_cost_line_ids]
        res = self.pool.get('ir.actions.act_window').for_xml_id(
            cr, uid, 'account', 'action_account_tree1', context)
        res['domain'] = "[('id', 'in', ["+','.join(
                    map(str, bill_lines))+"])]"
        return res

    def action_open_fy_material_lines(self, cr, uid, ids, context=None):
        """
        :return dict: dictionary value for created view
        """
        if context is None:
            context = {}
        line = self.browse(cr, uid, ids[0], context)
        bill_lines = [x.id for x in line.fy_actual_material_line_ids]
        res = self.pool.get('ir.actions.act_window').for_xml_id(
            cr, uid, 'account', 'action_account_tree1', context)
        res['domain'] = "[('id', 'in', ["+','.join(
                    map(str, bill_lines))+"])]"
        return res

    def action_open_fy_labor_lines(self, cr, uid, ids, context=None):
        """
        :return dict: dictionary value for created view
        """
        if context is None:
            context = {}
        line = self.browse(cr, uid, ids[0], context)
        bill_lines = [x.id for x in line.fy_actual_labor_line_ids]
        res = self.pool.get('ir.actions.act_window').for_xml_id(
            cr, uid, 'account', 'action_account_tree1', context)
        res['domain'] = "[('id', 'in', ["+','.join(
                    map(str, bill_lines))+"])]"
        return res

    def action_open_fy_billings_lines(self, cr, uid, ids, context=None):
        """
        :return dict: dictionary value for created view
        """
        if context is None:
            context = {}
        line = self.browse(cr, uid, ids[0], context)
        bill_lines = [x.id for x in line.fy_billings_line_ids]
        res = self.pool.get('ir.actions.act_window').for_xml_id(
            cr, uid, 'account', 'action_account_tree1', context)
        res['domain'] = "[('id', 'in', ["+','.join(
                    map(str, bill_lines))+"])]"
        return res
