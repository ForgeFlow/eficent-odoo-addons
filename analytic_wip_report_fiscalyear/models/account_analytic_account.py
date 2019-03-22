# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons import decimal_precision as dp
from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DT


class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    @api.multi
    def _compute_fy_wip_report(self):
        for account in self:
            all_ids = account.get_child_accounts().keys()
            # Total Value
            query_params = [tuple(all_ids)]
            query_params_fy = [tuple(all_ids)]
            query_params_fy_end = [tuple(all_ids)]
            where_date_fy = ''
            where_date_fy_end = ''
            where_date = ''
            context = self._context
            cr = self._cr
            if self._context.get('from_date_fy', False):
                from_date = context['from_date_fy']
                fromdatefy = datetime.strptime(
                    from_date, DT) - relativedelta(days=1)
                fromdatefy = datetime.strftime(fromdatefy, DT)
                where_date += " AND l.date >= %s"
                query_params += [from_date]
                where_date_fy += " AND l.date <= %s"
                query_params_fy += [fromdatefy]

            if self._context.get('to_date_fy', False):
                to_date = context['to_date_fy']
                where_date += " AND l.date <= %s"
                query_params += [to_date]
                where_date_fy_end += " AND l.date <= %s"
                query_params_fy_end += [to_date]

            # Total Value Beginning year
            cr.execute(
                """SELECT COALESCE(sum(amount),0.0) AS total_value
                FROM account_analytic_line_plan AS L
                LEFT JOIN account_analytic_account AS A
                ON L.account_id = A.id
                INNER JOIN account_account AC
                ON L.general_account_id = AC.id
                INNER JOIN account_account_type AT
                ON AT.id = AC.user_type_id
                WHERE AT.name in ('Income', 'Other Income')
                AND l.account_id IN %s
                AND a.active_analytic_planning_version = l.version_id
                """ + where_date_fy + """
                """,
                query_params_fy)
            val = cr.fetchone()[0] or 0
            account.total_value_fy = val

            # Total Value end year
            cr.execute(
                """SELECT COALESCE(sum(amount),0.0) AS total_value
                FROM account_analytic_line_plan AS L
                LEFT JOIN account_analytic_account AS A
                ON L.account_id = A.id
                INNER JOIN account_account AC
                ON L.general_account_id = AC.id
                INNER JOIN account_account_type AT
                ON AT.id = AC.user_type_id
                WHERE AT.name in ('Income', 'Other Income')
                AND l.account_id IN %s
                AND a.active_analytic_planning_version = l.version_id
                """ + where_date_fy_end + """
                """,
                query_params_fy_end)
            val = cr.fetchone()[0] or 0
            account.total_value_end_fy = val

            # actual cost at the the beginning of the fy
            cr.execute(
                """
                SELECT COALESCE(-1*sum(amount),0.0) total
                FROM account_analytic_line L
                INNER JOIN account_analytic_journal AAJ
                ON AAJ.id = L.journal_id
                INNER JOIN account_account AC
                ON L.general_account_id = AC.id
                INNER JOIN account_account_type AT
                ON AT.id = AC.user_type_id
                WHERE AT.name in ('Expense', 'Cost of Goods Sold',
                'Expenses', 'Cost of Revenue')
                AND L.account_id in %s
                """ + where_date_fy + """
                """, query_params_fy)
            account.actual_costs_fy = 0
            val = cr.fetchone()[0] or 0
            account.actual_costs_fy += val

            # actual cost at the the end of the fy
            cr.execute(
                """
                SELECT COALESCE(-1*sum(amount),0.0) total
                FROM account_analytic_line L
                INNER JOIN account_analytic_journal AAJ
                ON AAJ.id = L.journal_id
                INNER JOIN account_account AC
                ON L.general_account_id = AC.id
                INNER JOIN account_account_type AT
                ON AT.id = AC.user_type_id
                WHERE AT.name in ('Expense', 'Cost of Goods Sold',
                'Expenses', 'Cost of Revenue')
                AND L.account_id in %s
                """ + where_date_fy_end + """
                """, query_params_fy_end)
            account.actual_costs_end_fy = 0
            val = cr.fetchone()[0] or 0
            account.actual_costs_end_fy += val

            # Total estimated costs at the beginning of the fy
            cr.execute("""
            SELECT COALESCE(-1*sum(amount),0.0) AS total_value
            FROM account_analytic_line_plan AS L
            LEFT JOIN account_analytic_account AS A
            ON L.account_id = A.id
            INNER JOIN account_account AC
            ON L.general_account_id = AC.id
            INNER JOIN account_account_type AT
            ON AT.id = AC.user_type_id
            WHERE AT.name in ('Expense', 'Cost of Goods Sold',
            'Expenses', 'Cost of Revenue')
            AND L.account_id IN %s
            AND A.active_analytic_planning_version = L.version_id
            """ + where_date_fy + """
            """, query_params_fy)
            val = cr.fetchone()[0] or 0
            account.total_estimated_costs_fy = val

            # Total estimated costs at the enf of the fy
            cr.execute("""
            SELECT COALESCE(-1*sum(amount),0.0) AS total_value
            FROM account_analytic_line_plan AS L
            LEFT JOIN account_analytic_account AS A
            ON L.account_id = A.id
            INNER JOIN account_account AC
            ON L.general_account_id = AC.id
            INNER JOIN account_account_type AT
            ON AT.id = AC.user_type_id
            WHERE AT.name in ('Expense', 'Cost of Goods Sold',
            'Expenses', 'Cost of Revenue')
            AND L.account_id IN %s
            AND A.active_analytic_planning_version = L.version_id
            """ + where_date_fy_end + """
            """, query_params_fy_end)
            val = cr.fetchone()[0] or 0
            account.total_estimated_costs_end_fy = val

            try:
                account.percent_complete_fy = (
                    (account.actual_costs_fy /
                     account.total_estimated_costs_fy) * 100)
            except ZeroDivisionError:
                account.percent_complete_fy = 0

            try:
                account.percent_complete_end_fy = (
                    (account.actual_costs_end_fy /
                     account.total_estimated_costs_end_fy) * 100)
            except ZeroDivisionError:
                account.percent_complete_end_fy = 0

            # Earned revenue
            account.earned_revenue_fy = \
                account.percent_complete_fy/100 * account.total_value_fy
            account.earned_revenue_end_fy = \
                account.percent_complete_end_fy/100 * \
                account.total_value_end_fy
            account.fy_revenue = \
                account.earned_revenue_end_fy - account.earned_revenue_fy
#
            # Actual costs for the period
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
                WHERE AT.name in ('Expense', 'Cost of Goods Sold',
               'Expenses', 'Cost of Revenue')
                AND L.account_id IN %s
                """ + where_date_fy + """
                """, query_params_fy)
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
                    'Income', 'Other Income')
                AND L.account_id IN %s
                """ + where_date + """
                """, query_params
            )
            fy_billings_line_ids = []
            for (total, line_id) in cr.fetchall():
                account.fy_billings += total
                fy_billings_line_ids.append(line_id)

            account.fy_billings_line_ids = [
                (6, 0, [l for l in fy_billings_line_ids])]
            # Gross margin
            account.fy_gross_profit = (account.fy_revenue -
                                       account.fy_actual_costs)
        return True

    total_value_fy = fields.Float(
        compute='_compute_fy_wip_report',
        string='Total Value at beginning year',
        help='Only for revenue calculation',
        digits=dp.get_precision('Account')
    )
    total_value_end_fy = fields.Float(
        compute='_compute_fy_wip_report',
        string='Total Value at end year',
        help='Only for revenue calculation',
        digits=dp.get_precision('Account')
    )
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
        help='Based on prior year revenue',
        digits=dp.get_precision('Account')
    )
    earned_revenue_fy = fields.Float(
        compute='_compute_fy_wip_report',
        string='Revenue at the Beginning of the Fiscal Year',
        help='Only for revenue calculation',
        digits=dp.get_precision('Account')
    )
    earned_revenue_end_fy = fields.Float(
        compute='_compute_fy_wip_report',
        string='Revenue at the end of the Fiscal Year',
        help='Only for revenue calculation',
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
    actual_costs_fy = fields.Float(
        compute='_compute_wip_report',
        string='Actual Costs to date beginning FY',
        digits=dp.get_precision('Account')
    )
    actual_costs_end_fy = fields.Float(
        compute='_compute_wip_report',
        string='Actual Costs to date end FY',
        digits=dp.get_precision('Account')
    )
    total_estimated_costs_fy = fields.Float(
        compute='_compute_wip_report',
        string='Total Estimated Costs Beginning FY',
        digits=dp.get_precision('Account')
    )
    total_estimated_costs_end_fy = fields.Float(
        compute='_compute_wip_report',
        string='Total Estimated Costs end FY',
        digits=dp.get_precision('Account')
    )
    percent_complete_fy = fields.Float(
        compute='_compute_wip_report',
        string='Percent Complete beginning FY',
        digits=(16, 10.0)
    )
    percent_complete_end_fy = fields.Float(
        compute='_compute_wip_report',
        string='Percent Complete ending FY',
        digits=(16, 10.0)
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
