# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm


class AccountsWithContractValue(orm.TransientModel):
    _name = "accounts.with.contract.value"
    _description = "Analytic Accounts with Contract Value"
    _columns = {
        'item_ids': fields.one2many('accounts.with.contract.value.item',
                                    'wiz_id',
                                    string="Accounts with Contract Value")
    }

    def _prepare_item(self, cr, uid, account, context=None):
        return [{
            'account_id': account.id,
            'contract_value': account.contract_value,
        }]

    def default_get(self, cr, uid, fields, context=None):
        res = super(AccountsWithContractValue, self).default_get(
            cr, uid, fields, context=context)
        analytic_obj = self.pool['account.analytic.account']
        analytic_ids = context.get('active_ids', [])
        active_model = context.get('active_model')

        if not analytic_ids:
            return res
        assert active_model == 'account.analytic.account', \
            'Bad context propagation'

        items = []
        accs = analytic_obj.list_accounts_with_contract_value(
            cr, uid, analytic_ids, context=context)

        for acc_id in accs.keys():
                for ch_acc in analytic_obj.browse(cr, uid, accs[acc_id].keys(),
                                                  context=context):
                    items += self._prepare_item(cr, uid, ch_acc,
                                                context=context)
        res['item_ids'] = items

        return res


class AccountsWithContractValueItem(orm.TransientModel):
    _name = "accounts.with.contract.value.item"
    _description = "Analytic Accounts with Contract Value Items"

    _columns = {
        'wiz_id': fields.many2one(
            'accounts.with.contract.value',
            'Wizard', required=True, ondelete='cascade',
            readonly=True),

        'account_id': fields.many2one('account.analytic.account',
                                      'Analytic Account',
                                      required=True,
                                      readonly=True),

        'contract_value': fields.float('Contract Value')
    }
