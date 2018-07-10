# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class AccountAnalyticPlanJournal(models.Model):
    _inherit = 'account.analytic.plan.journal'

    cost_type = fields.Selection(
        [('labor', 'Labor Cost'),
         ('material', 'Material Cost'),
         ('revenue', 'Revenue')], "Type of cost")


class AnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    def _get_plan_journal_item_totals(self, journal_ids, analytic_account_ids):
        line_obj = self.env['account.analytic.line.plan']
        res = 0.0
        for analytic_account in analytic_account_ids:
            plan_version = self.env['account.analytic.account'].browse(
                analytic_account[0]).active_analytic_planning_version
            domain = [('journal_id', 'in', journal_ids),
                      ('account_id', '=', analytic_account[0]),
                      ('version_id', '=', plan_version.id)]

            if self.env.context.get('from_date', False):
                domain.append(('date', '>=', self.env.context['from_date']))
            if self.env.get('to_date', False):
                domain.append(('date', '<=', self.env.context['to_date']))

            accs = line_obj.search(domain)
            res = 0.0
            for acc in accs:
                res += acc['amount']
        return res

    @api.multi
    def get_analytic_plan_totals(self):

        journal_obj = self.env['account.analytic.plan.journal']
        labor_journal_ids = journal_obj.search(
            [('cost_type', '=', 'labor')])
        material_journal_ids = journal_obj.search(
            [('cost_type', '=', 'material')])
        revenue_journal_ids = journal_obj.search(
            [('cost_type', '=', 'revenue')])

        for account in self:
            analytic_account_ids = account._get_all_analytic_accounts()
            if labor_journal_ids:
                account.labor_cost_plan = -1 * \
                    self._get_plan_journal_item_totals(
                        labor_journal_ids.ids, analytic_account_ids)
            else:
                account.labor_cost_plan = 0.0
            if material_journal_ids:
                account.material_cost_plan = -1 * \
                    self._get_plan_journal_item_totals(
                        material_journal_ids.ids, analytic_account_ids)
            else:
                account.material_cost_plan = 0.0

            if revenue_journal_ids:
                account.revenue_plan = \
                    self._get_plan_journal_item_totals(
                        revenue_journal_ids.ids, analytic_account_ids)
            else:
                account.revenue_plan = 0.0

            account.total_cost_plan = \
                account.material_cost_plan + account.labor_cost_plan

            account.gross_profit_plan = \
                account.revenue_plan - account.total_cost_plan

    labor_cost_plan = fields.Float(
        compute=get_analytic_plan_totals,
        string='Planned Labor cost',
        digits=dp.get_precision('Account'))
    material_cost_plan = fields.Float(
        compute=get_analytic_plan_totals,
        string='Planned Material cost',
        digits=dp.get_precision('Account'))
    total_cost_plan = fields.Float(
        compute=get_analytic_plan_totals,
        string='Planned total cost',
        digits=dp.get_precision('Account'))
    revenue_plan = fields.Float(
        compute=get_analytic_plan_totals, string='Planned Revenue',
        digits=dp.get_precision('Account'))
    gross_profit_plan = fields.Float(
        compute=get_analytic_plan_totals,
        string='Planned Gross Profit',
        digits=dp.get_precision('Account'))
