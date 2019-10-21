# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class AccountAnalyticPlanJournal(models.Model):
    _inherit = "account.analytic.plan.journal"

    cost_type = fields.Selection(
        [
            ("labor", "Labor Cost"),
            ("material", "Material Cost"),
            ("revenue", "Revenue"),
        ],
        "Type of cost",
    )


class AnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    def _get_plan_journal_item_totals(
        self, journal_ids, analytic_account_ids, version_id
    ):
        line_obj = self.env["account.analytic.line.plan"]
        res = 0.0
        domain = [("journal_id", "in", journal_ids)]
        if analytic_account_ids:
            domain.append(("account_id", "in", analytic_account_ids))
        else:
            return res
        if version_id:
            domain.append(("version_id", "=", version_id))
        domain.append(
            (
                "company_id",
                "=",
                self.browse(analytic_account_ids[0]).company_id.id,
            )
        )
        accs = line_obj.read_group(
            domain, fields=["amount", "company_id"], groupby="company_id"
        )
        if accs:
            res = accs[0]["amount"]
        return res

    @api.multi
    def compute_total_cost_plan(self):
        for account in self:
            account.total_cost_plan = (
                account.material_cost_plan + account.labor_cost_plan
            )

    @api.multi
    def compute_cost_revenue_plan(self):
        journal_obj = self.env["account.analytic.plan.journal"]
        revenue_journal_ids = journal_obj.search(
            [("cost_type", "=", "revenue")]
        )
        material_journal_ids = journal_obj.search(
            [("cost_type", "=", "material")]
        )
        labor_journal_ids = journal_obj.search([("cost_type", "=", "labor")])
        for account in self:
            analytic_account_ids = account._get_all_analytic_accounts()
            if revenue_journal_ids:
                account.revenue_plan = self._get_plan_journal_item_totals(
                    revenue_journal_ids.ids,
                    analytic_account_ids,
                    account.active_analytic_planning_version.id,
                )
            else:
                account.revenue_plan = 0.0

            if material_journal_ids:
                account.material_cost_plan = (
                    -1
                    * self._get_plan_journal_item_totals(
                        material_journal_ids.ids,
                        analytic_account_ids,
                        account.active_analytic_planning_version.id,
                    )
                )
            else:
                account.material_cost_plan = 0.0
            if labor_journal_ids:
                account.labor_cost_plan = (
                    -1
                    * self._get_plan_journal_item_totals(
                        labor_journal_ids.ids,
                        analytic_account_ids,
                        account.active_analytic_planning_version.id,
                    )
                )
            else:
                account.labor_cost_plan = 0.0

    @api.multi
    @api.depends("total_cost_plan", "revenue_plan")
    def compute_gross_profit_plan(self):
        for account in self:
            account.gross_profit_plan = (
                account.revenue_plan + account.total_cost_plan
            )

    labor_cost_plan = fields.Float(
        compute=compute_cost_revenue_plan,
        string="Planned Labor cost",
        digits=dp.get_precision("Account"),
    )
    material_cost_plan = fields.Float(
        compute=compute_cost_revenue_plan,
        string="Planned Material cost",
        digits=dp.get_precision("Account"),
    )
    total_cost_plan = fields.Float(
        compute=compute_total_cost_plan,
        string="Planned total cost",
        digits=dp.get_precision("Account"),
    )
    revenue_plan = fields.Float(
        compute=compute_cost_revenue_plan,
        string="Planned Revenue",
        digits=dp.get_precision("Account"),
    )
    gross_profit_plan = fields.Float(
        compute=compute_gross_profit_plan,
        string="Planned Gross Profit",
        digits=dp.get_precision("Account"),
    )
