# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class AccountAnalyticJournal(models.Model):
    _inherit = 'account.analytic.journal'

    cost_type = fields.Selection(
        [('labor', 'Labor Cost'),
         ('material', 'Material Cost'),
         ('revenue', 'Revenue')], "Type of cost")


class AnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def _get_all_analytic_accounts(self):
        # Now add the children
        self.env.cr.execute('''
        WITH RECURSIVE children AS (
        SELECT parent_id, id
        FROM account_analytic_account
        WHERE parent_id in %s
        UNION ALL
        SELECT a.parent_id, a.id
        FROM account_analytic_account a
        JOIN children b ON(a.parent_id = b.id)
        )
        SELECT id FROM children order by parent_id
        ''', (tuple(self.ids),))
        res = self.env.cr.fetchall()
        return res

    def _get_journal_item_totals(self, journal_ids, analytic_account_ids):
        line_obj = self.env['account.analytic.line']
        domain = [('journal_id', 'in', journal_ids.ids)]
        if analytic_account_ids:
            domain.append(('account_id', 'in', analytic_account_ids))
        if self.env.context.get('from_date', False):
            domain.append(('date', '>=', self.env.context['from_date']))
        if self.env.context.get('to_date', False):
            domain.append(('date', '<=', self.env.context['to_date']))
        accs = line_obj.search(domain)
        res = 0.0
        for acc in accs:
            res += acc.amount
        return res

    @api.multi
    @api.depends('balance')
    def get_analytic_totals(self):
        journal_obj = self.env['account.analytic.journal']

        labor_journal_ids = journal_obj.search(
            [('cost_type', '=', 'labor')])
        material_journal_ids = journal_obj.search(
            [('cost_type', '=', 'material')])
        revenue_journal_ids = journal_obj.search(
            [('cost_type', '=', 'revenue')])

        for account in self:
            analytic_account_ids = account._get_all_analytic_accounts()
            account.labor_cost = -1*self._get_journal_item_totals(
                labor_journal_ids, analytic_account_ids)
            account.material_cost = -1*self._get_journal_item_totals(
                material_journal_ids, analytic_account_ids)
            account.revenue = self._get_journal_item_totals(
                revenue_journal_ids, analytic_account_ids)
            account.total_cost = account.material_cost + account.labor_cost
            account.gross_profit = account.revenue - account.total_cost
        return True

    labor_cost = fields.Float(
        compute=get_analytic_totals,
        store=True,
        string='Labor cost',
        digits=dp.get_precision('Account'))
    material_cost = fields.Float(
        compute=get_analytic_totals, string='Material cost',
        store=True,
        digits=dp.get_precision('Account'))
    total_cost = fields.Float(
        compute=get_analytic_totals, string='Total cost',
        store=True,
        digits=dp.get_precision('Account'))
    revenue = fields.Float(
        compute=get_analytic_totals, string='Revenue',
        store=True,
        digits=dp.get_precision('Account'))
    gross_profit = fields.Float(
        compute=get_analytic_totals,
        store=True,
        string='Gross Profit',
        digits=dp.get_precision('Account'))
