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
                'fy_costs': 0,
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
            cr.execute(
                """
                SELECT COALESCE(-1*sum(amount),0.0)
                                FROM account_analytic_line L
                                INNER JOIN account_account AC
                                ON L.general_account_id = AC.id
                                INNER JOIN account_account_type AT
                                ON AT.id = AC.user_type_id
                                WHERE AT.name in ('Expense', 'Cost of Goods Sold')
                                AND L.account_id IN %s
                """ + where_date + """
                """,
                query_params
            )
            val = cr.fetchone()[0] or 0
            res[account.id]['fy_costs'] = val

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
            res[account.id]['fy_revenue'] = val

            # Gross margin
            res[account.id]['fy_gross_profit'] = \
                res[account.id]['fy_revenue'] - res[account.id]['fy_costs']
        return res

    fy_costs = fields.Float(
        compute='_fy_wip_report',
        string='Actual Costs to date',
        digits=dp.get_precision('Account')
    )

    fy_gross_profit = fields.Float(
        compute='_fy_wip_report',
        string='Estimated Gross Profit',
        help="""Total Value – Total Estimated Costs""",
        digits=dp.get_precision('Account')
    )
    fy_revenue = fields.Float(
        compute='_fy_wip_report',
        string='Earned Revenue to date',
        help="Fiscal Year Revenue",
        digits=dp.get_precision('Account')
    )
