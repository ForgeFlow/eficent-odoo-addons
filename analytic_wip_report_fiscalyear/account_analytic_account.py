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
                               'fy_actual_costs': 0,
                               'fy_actual_material_cost': 0,
                               'fy_actual_labor_cost': 0,
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
            res[account.id]['fy_revenue_line_ids'] = []
            for (val, line_id) in cr.fetchall():
                res[account.id]['fy_revenue'] += val
                res[account.id]['fy_revenue_line_ids'].append(line_id)

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
                if cost_type == 'material':
                    res[account.id]['fy_actual_material_cost'] -=total
                    res[account.id]['fy_actual_material_line_ids'].append(line_id)
                elif cost_type == 'labor':
                    res[account.id]['fy_actual_labor_cost'] -= total
                    res[account.id]['fy_actual_labor_line_ids'].append(line_id)
                res[account.id]['fy_actual_costs'] -= total
                res[account.id]['fy_actual_cost_line_ids'].append(line_id)

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

        'fy_actual_costs': fields.function(
            _wip_report_fy, method=True, type='float',
            string='Fiscal Year Actual Costs', multi='wip_report_fy',
            digits_compute=dp.get_precision('Account')),

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
        'fy_revenue_line_ids': fields.function(
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

    def action_open_fy_revenue_lines(self, cr, uid, ids, context=None):
        """
        :return dict: dictionary value for created view
        """
        if context is None:
            context = {}
        line = self.browse(cr, uid, ids[0], context)
        bill_lines = [x.id for x in line.fy_revenue_line_ids]
        res = self.pool.get('ir.actions.act_window').for_xml_id(
            cr, uid, 'account', 'action_account_tree1', context)
        res['domain'] = "[('id', 'in', ["+','.join(
                    map(str, bill_lines))+"])]"
        return res