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
    @api.depends('contract_value')
    def _compute_total_contract_value(self):
        for acc_id in self:
            total_contract_value = 0.0
            if type(acc_id.id) == int:
                # _get_all_analytic_accounts fails for new objects
                accs = acc_id._get_all_analytic_accounts()
                for ch_acc_id in self.browse(accs):
                    total_contract_value += ch_acc_id.contract_value
            acc_id.total_contract_value = total_contract_value

    contract_value = fields.Float(
        'Original Contract Value',
        readonly=True)
    total_contract_value = fields.Float(
        compute=_compute_total_contract_value,
        string='Current Total Contract Value',
        help='Total Contract Value including child analytic accounts')
