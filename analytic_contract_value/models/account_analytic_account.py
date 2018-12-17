# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from itertools import chain


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def _get_all_analytic_accounts(self):
        # Now add the children
        query = '''
        WITH RECURSIVE children AS (
        SELECT parent_id, id
        FROM account_analytic_account
        WHERE parent_id in ({id1}) or id in ({id1})
        UNION ALL
        SELECT a.parent_id, a.id
        FROM account_analytic_account a
        JOIN children b ON(a.parent_id = b.id)
        )
        SELECT id FROM children order by parent_id
        '''
        query = query.format(id1=', '.join([str(i) for i in self._ids]))
        self.env.cr.execute(query)
        res = self.env.cr.fetchall()
        res_list = list(chain(*res))
        return list(set(res_list))

    @api.multi
    def _compute_contract_value(self):
        for acc_id in self:
            all_ids = acc_id._get_all_analytic_accounts()
            query_params = [tuple(all_ids)]
            self.env.cr.execute(
                """
                SELECT COALESCE(sum(amount),0.0)
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
                """,
                query_params)
            val = self.env.cr.fetchone()[0] or 0
            acc_id.contract_value = val
        return True

    contract_value = fields.Float(
        compute=_compute_contract_value,
        string='Current Total Contract Value',
        help='Total Contract Value including child analytic accounts')
