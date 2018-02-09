# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
import odoo.addons.decimal_precision as dp


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def list_accounts_with_contract_value(self):
        res = {}
        for rec in self:
            curr_id = rec.d
            all_acc = []
            res[curr_id] = {}
            # Now add the children
            cr.execute('''
            WITH RECURSIVE children AS (
            SELECT parent_id, id
            FROM account_analytic_account
            WHERE parent_id = %s
            UNION ALL
            SELECT a.parent_id, a.id
            FROM account_analytic_account a
            JOIN children b ON(a.parent_id = b.id)
            )
            SELECT * FROM children order by parent_id
            ''', (curr_id,))
            cr_res = cr.fetchall()
            for x, y in cr_res:
                all_acc.append(y)
            all_acc.append(curr_id)
            for account in self:
                if account and account.contract_value:
                    res[curr_id][account.id] = account.contract_value
        return res

    @api.multi
    def _total_contract_value_calc(self):
        res = {}
        acc_list = self.list_accounts_with_contract_value()
        for acc_id in acc_list.keys():
            res[acc_id] = 0.0
            for ch_acc_id in acc_list[acc_id]:
                res[acc_id] += acc_list[acc_id][ch_acc_id]
        return res

    contract_value = fields.Float(
        'Original Contract Value',
        track_visibility='onchange',
        readonly=True)
    total_contract_value = fields.Float(
            compute=_total_contract_value_calc,
            string='Current Total Contract Value',
            help='Total Contract Value including child analytic accounts')
