# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AnalyticContractValueBreakdown(models.TransientModel):
    _name = "accounts.with.contract.value"
    _description = "Change Contract Value"
    _description = "Analytic Accounts with Contract Value"

    item_ids = fields.One2many(
        'accounts.with.contract.value.item', 'wiz_id',
        string="Accounts with Contract Value")

    @api.model
    def _prepare_item(self, account):
        return [(0, 0, {
            'account_id': account.id,
            'contract_value': account.contract_value})]

    @api.model
    def default_get(self, fields):
        res = super(AnalyticContractValueBreakdown, self).default_get(fields)
        analytic_obj = self.env['account.analytic.account']
        analytic_id = self.env.context.get('active_id', [])
        active_model = self.env.context.get('active_model')

        if not analytic_id:
            return res
        assert active_model == 'account.analytic.account', \
            'Bad context propagation'

        items = []
        acc = analytic_obj.browse(analytic_id)
        accs = acc._get_all_analytic_accounts()
        for acc in analytic_obj.browse(accs):
            items += self._prepare_item(acc)
        res['item_ids'] = items
        return res


class AccountsWithContractValueItem(models.TransientModel):
    _name = "accounts.with.contract.value.item"
    _description = "Analytic Accounts with Contract Value Items"

    wiz_id = fields.Many2one(
        'accounts.with.contract.value',
        'Wizard', required=True, ondelete='cascade',
        readonly=True)

    account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account', required=True, readonly=True)

    contract_value = fields.Float('Contract Value')
