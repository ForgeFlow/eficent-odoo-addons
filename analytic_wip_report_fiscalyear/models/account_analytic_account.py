# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons import decimal_precision as dp
from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    @api.multi
    def _compute_fy_wip_report(self):
        for account in self:
            all_ids = account.get_child_accounts().keys()
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
            # pylint: disable=sql-injection
            cr.execute(
                """
                SELECT amount, L.id, AAJ.cost_type
                                FROM account_analytic_line L
                                INNER JOIN account_analytic_journal AAJ
                                ON AAJ.id = L.journal_id
                                INNER JOIN account_account AC
                                ON L.general_account_id = AC.id
                                INNER JOIN account_account_type AT
                                ON AT.id = AC.user_type_id
                                WHERE AT.name in (
                                'Expense', 'Cost of Goods Sold')
                                AND L.account_id IN %s
                """ + where_date + """
                """, query_params)
            account.fy_actual_costs = 0
            fy_actual_cost_line_ids = []
            fy_actual_material_line_ids = []
            fy_actual_labor_line_ids = []
            for (total, line_id, cost_type) in cr.fetchall():
                if cost_type in ('material', 'revenue'):
                    account.fy_actual_material_cost -= total
                    fy_actual_material_line_ids.append(line_id)
                elif cost_type == 'labor':
                    account.fy_actual_labor_cost -= total
                    fy_actual_labor_line_ids.append(line_id)
                account.fy_actual_costs -= total
                fy_actual_cost_line_ids.append(line_id)
            account.fy_actual_cost_line_ids = [
                (6, 0, [l for l in fy_actual_cost_line_ids])]
            account.fy_actual_material_line_ids = [
                (6, 0, [l for l in fy_actual_material_line_ids])]
            account.fy_actual_labor_line_ids = [
                (6, 0, [l for l in fy_actual_labor_line_ids])]

            # Actual billings to date
            # pylint: disable=sql-injection
            cr.execute(
                """
                SELECT amount, L.id
                FROM account_analytic_line L
                INNER JOIN account_account AC
                ON L.general_account_id = AC.id
                INNER JOIN account_account_type AT
                ON AT.id = AC.user_type_id
                WHERE AT.name in (
                    'Income', 'Other Income', 'Other Current Asset')
                AND L.account_id IN %s
                """ + where_date + """
                """, query_params
            )
            fy_billings_line_ids = []
            for (total, line_id) in cr.fetchall():
                account.fy_billings += total
                fy_billings_line_ids.append(line_id)

            account.fy_revenue = (account.fy_billings + account.under_billings
                                  - account.over_billings)
            account.fy_billings_line_ids = [
                (6, 0, [l for l in fy_billings_line_ids])]
            # Gross margin
            account.fy_gross_profit = (account.fy_revenue -
                                       account.fy_actual_costs)
        return True

    fy_actual_costs = fields.Float(
        compute='_compute_fy_wip_report',
        string='Fiscal Year Costs',
        digits=dp.get_precision('Account')
    )

    fy_actual_material_cost = fields.Float(
        compute='_compute_fy_wip_report',
        string='Fiscal Year Material Costs',
        digits=dp.get_precision('Account')
    )

    fy_actual_labor_cost = fields.Float(
        compute='_compute_fy_wip_report',
        string='Fiscal Year Labor Costs',
        digits=dp.get_precision('Account')
    )

    fy_gross_profit = fields.Float(
        compute='_compute_fy_wip_report',
        string='Estimated Gross Profit',
        help="""Total Value – Total Estimated Costs""",
        digits=dp.get_precision('Account')
    )
    fy_billings = fields.Float(
        compute='_compute_fy_wip_report',
        string='Fiscal Year Billings',
        digits=dp.get_precision('Account')
    )
    fy_revenue = fields.Float(
        compute='_compute_fy_wip_report',
        string='Fiscal Year Revenue',
        digits=dp.get_precision('Account')
    )
    fy_actual_cost_line_ids = fields.Many2many(
        comodel_name="account.analytic.line",
        compute='_compute_fy_wip_report',
        string='Detail',
    )
    fy_actual_labor_line_ids = fields.Many2many(
        comodel_name="account.analytic.line",
        compute='_compute_fy_wip_report',
        string='Detail',
    )
    fy_actual_material_line_ids = fields.Many2many(
        comodel_name="account.analytic.line",
        compute='_compute_fy_wip_report',
        string='Detail',
    )
    fy_billings_line_ids = fields.Many2many(
        comodel_name="account.analytic.line",
        compute='_compute_fy_wip_report',
        string='Detail',
    )

    @api.multi
    def action_open_fy_cost_lines(self):
        line = self
        bill_lines = [x.id for x in line.fy_actual_cost_line_ids]
        res = self.env['ir.actions.act_window'].for_xml_id(
            'analytic', 'account_analytic_line_action_entries')
        res['domain'] = "[('id', 'in', ["+','.join(
            map(str, bill_lines))+"])]"
        return res

    @api.multi
    def action_open_fy_material_lines(self):
        line = self
        bill_lines = [x.id for x in line.fy_actual_material_line_ids]
        res = self.env['ir.actions.act_window'].for_xml_id(
            'analytic', 'account_analytic_line_action_entries')
        res['domain'] = "[('id', 'in', ["+','.join(
            map(str, bill_lines))+"])]"
        return res

    @api.multi
    def action_open_fy_labor_lines(self):
        line = self
        bill_lines = [x.id for x in line.fy_actual_labor_line_ids]
        res = self.env['ir.actions.act_window'].for_xml_id(
            'analytic', 'account_analytic_line_action_entries')
        res['domain'] = "[('id', 'in', ["+','.join(
            map(str, bill_lines))+"])]"
        return res

    @api.multi
    def action_open_fy_billings_lines(self):
        line = self
        bill_lines = [x.id for x in line.fy_billings_line_ids]
        res = self.env['ir.actions.act_window'].for_xml_id(
            'analytic', 'account_analytic_line_action_entries')
        res['domain'] = "[('id', 'in', ["+','.join(
            map(str, bill_lines))+"])]"
        return res
