# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, orm
import openerp.addons.decimal_precision as dp


class AccountAnalyticAccount(orm.Model):
    _inherit = 'account.analytic.account'

    def _contract_value_calc(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        res = {}

        for acc_id in self.browse(cr, uid, ids):
            res[acc_id.id] = 0.0
            all_ids = self.get_child_accounts(cr, uid, [acc_id.id]).keys()
            query_params = [tuple(all_ids)]
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
                """,
                query_params)
            val = cr.fetchone()[0] or 0
            res[acc_id.id] = val
        return res

    _columns = {
        'contract_value': fields.function(
            _contract_value_calc, method=True, type='float',
            track_visibility='onchange',
            string='Current Total Contract Value',
            help='Total Contract Value including child analytic accounts')
    }
