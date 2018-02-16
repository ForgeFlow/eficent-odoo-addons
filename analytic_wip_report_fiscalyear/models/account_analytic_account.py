# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons import decimal_precision as dp
from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    @api.multi
    def _fy_wip_report(self):
        res = {}
        for account in self:
            all_ids = self.get_child_accounts().keys()
            res[account.id] = {
                'fy_actual_costs': 0,
                'fy_actual_costs': 0,
                'fy_actual_material_cost': 0,
                'fy_actual_labor_cost': 0,
                'fy_billings': 0,
                'fy_revenue': 0,
                'fy_gross_profit': 0,
            }
            # Total Value
            query_params = [tuple(all_ids)]
            where_date = ''
            context = self._context
            cr = self._cr
            if self._context.get('from_date_fy', False):
                from_date = context['from_date_fy']
                where_date += " AND l.date >= %s"
                query_params += [from_date]
            if self._context.get('to_date_fy', False):
                to_date = context['to_date_fy']
                where_date += " AND l.date <= %s"
                query_params += [to_date]

            # Actual costs to date
            cr.execute(
                """
                SELECT amount, L.id, AAJ.type
                                FROM account_analytic_line L
                                INNER JOIN account_analytic_journal AAJ
                                ON AAJ.id = L.journal_id
                                INNER JOIN account_account AC
                                ON L.general_account_id = AC.id
                                INNER JOIN account_account_type AT
                                ON AT.id = AC.user_type_id
                                WHERE AT.name in ('Expense', 'Cost of Goods Sold')
                                AND L.account_id IN %s
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
            # Actual billings to date
            cr.execute(
                """
                SELECT COALESCE(sum(amount),0.0)
                FROM account_analytic_line L
                INNER JOIN account_account AC
                ON L.general_account_id = AC.id
                INNER JOIN account_account_type AT
                ON AT.id = AC.user_type_id
                WHERE AT.name in ('Income', 'Other Income', 'Other Current Asset')
                AND L.account_id IN %s
                """ + where_date + """
                """, query_params
            )
            val = cr.fetchone()[0] or 0
            res[account.id]['fy_billings'] = val

            # Gross margin
            res[account.id]['fy_gross_profit'] = \
                res[account.id]['fy_revenue'] - res[account.id]['fy_actual_costs']
        return res

    fy_actual_costs = fields.Float(
        compute='_fy_wip_report',
        string='Fiscal Year Costs',
        digits=dp.get_precision('Account')
    )

    fy_actual_material_cost = fields.Float(
        compute='_fy_wip_report',
        string='Fiscal Year Material Costs',
        digits=dp.get_precision('Account')
    )

    fy_actual_labor_cost = fields.Float(
        compute='_fy_wip_report',
        string='Fiscal Year Labor Costs',
        digits=dp.get_precision('Account')
    )

    fy_gross_profit = fields.Float(
        compute='_fy_wip_report',
        string='Estimated Gross Profit',
        help="""Total Value – Total Estimated Costs""",
        digits=dp.get_precision('Account')
    )
    fy_billings = fields.Float(
        compute='_fy_wip_report',
        string='Fiscal Year Billings',
        digits=dp.get_precision('Account')
    )
    fy_revenue = fields.Float(
        compute='_fy_wip_report',
        string='Fiscal Year Revenue',
        digits=dp.get_precision('Account')
    )
    fy_actual_cost_line_ids = fields.Many2many(
        comodel_name="account.analytic.line",
        compute='_fy_wip_report',
        string='Detail',
    )
    fy_actual_labor_line_ids = fields.Many2many(
        comodel_name="account.analytic.line",
        compute='_fy_wip_report',
        string='Detail',
    )
    fy_actual_material_line_ids = fields.Many2many(
        comodel_name="account.analytic.line",
        compute='_fy_wip_report',
        string='Detail',
    )
    fy_billings_line_ids = fields.Many2many(
        comodel_name="account.analytic.line",
        compute='_fy_wip_report',
        string='Detail',
    )

    @api.multi
    def action_open_fy_cost_lines(self):
        line = self
        bill_lines = [x.id for x in line.fy_actual_cost_line_ids]
        res = self.pool.get('ir.actions.act_window').for_xml_id(
            cr, uid, 'account', 'action_account_tree1', context)
        res['domain'] = "[('id', 'in', ["+','.join(
                    map(str, bill_lines))+"])]"
        return res

    @api.multi
    def action_open_fy_material_lines(self):
        line = self
        bill_lines = [x.id for x in line.fy_actual_material_line_ids]
        res = self.pool.get('ir.actions.act_window').for_xml_id(
            'account', 'action_account_tree1')
        res['domain'] = "[('id', 'in', ["+','.join(
                    map(str, bill_lines))+"])]"
        return res

    @api.multi
    def action_open_fy_labor_lines(self):
        line = self
        bill_lines = [x.id for x in line.fy_actual_labor_line_ids]
        res = self.pool.get('ir.actions.act_window').for_xml_id(
            'account', 'action_account_tree1')
        res['domain'] = "[('id', 'in', ["+','.join(
                    map(str, bill_lines))+"])]"
        return res

    @api.multi
    def action_open_fy_billings_lines(self):
        line = self
        bill_lines = [x.id for x in line.fy_billings_line_ids]
        res = self.pool.get('ir.actions.act_window').for_xml_id(
           'account', 'action_account_tree1')
        res['domain'] = "[('id', 'in', ["+','.join(
                    map(str, bill_lines))+"])]"
        return res
