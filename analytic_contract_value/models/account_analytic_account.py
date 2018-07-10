# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def list_children_accounts(self):
        res = {}
        for rec in self:
            curr_id = rec.id
            res[curr_id] = {}
            # Now add the children
            self.env.cr.execute('''
            WITH RECURSIVE children AS (
            SELECT parent_id, id
            FROM account_analytic_account
            WHERE parent_id = %s
            UNION ALL
            SELECT a.parent_id, a.id
            FROM account_analytic_account a
            JOIN children b ON(a.parent_id = b.id)
            )
            SELECT id FROM children order by parent_id
            ''', (curr_id,))
            cr_res = self.env.cr.fetchall()
        return cr_res

    @api.multi
    def _total_contract_value_calc(self):
        for acc_id in self:
            accs = acc_id.list_children_accounts()
            total_contract_value = 0.0
            for ch_acc_id in self.browse(accs):
                total_contract_value += ch_acc_id.contract_value
            acc_id.total_contract_value = total_contract_value

    contract_value = fields.Float(
        'Original Contract Value',
        track_visibility='onchange',
        readonly=True)
    total_contract_value = fields.Float(
        compute=_total_contract_value_calc,
        string='Current Total Contract Value',
        help='Total Contract Value including child analytic accounts')
