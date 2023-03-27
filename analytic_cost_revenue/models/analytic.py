# Copyright 2017 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from itertools import chain

from odoo import fields, models


class AccountAnalyticJournal(models.Model):
    _inherit = "account.analytic.journal"

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

    def _get_all_analytic_accounts(self):
        # Now add the children
        query = """
        WITH RECURSIVE children AS (
        SELECT parent_id, id
        FROM account_analytic_account
        WHERE parent_id in %s or id in %s
        UNION ALL
        SELECT a.parent_id, a.id
        FROM account_analytic_account a
        JOIN children b ON(a.parent_id = b.id)
        )
        SELECT id FROM children order by parent_id
        """
        self.env.cr.execute(query, (tuple(self._ids), tuple(self._ids)))
        res = self.env.cr.fetchall()
        res_list = list(chain(*res))
        return list(set(res_list))

    def _get_journal_item_totals(self, journal_ids, analytic_account_ids):
        line_obj = self.env["account.analytic.line"]
        domain = [("journal_id", "in", journal_ids.ids)]
        res = 0.0
        if analytic_account_ids:
            domain.append(("account_id", "in", analytic_account_ids))
        else:
            return res
        if self.env.context.get("from_date", False):
            domain.append(("date", ">=", self.env.context["from_date"]))
        if self.env.context.get("to_date", False):
            domain.append(("date", "<=", self.env.context["to_date"]))
        domain.append(
            ("company_id", "=", self.browse(analytic_account_ids[0]).company_id.id)
        )
        accs = line_obj.read_group(
            domain, fields=["amount", "company_id"], groupby="company_id"
        )
        if accs:
            res = accs[0]["amount"]
        return res

    def compute_total_cost(self):
        for account in self:
            account.total_cost = account.material_cost + account.labor_cost
        return True

    def compute_gross_profit(self):
        for account in self:
            account.gross_profit = account.revenue - account.total_cost
        return True

    def compute_cost_revenue(self):
        journal_obj = self.env["account.analytic.journal"]
        material_journal_ids = journal_obj.search([("cost_type", "=", "material")])
        revenue_journal_ids = journal_obj.search([("cost_type", "=", "revenue")])
        labor_journal_ids = journal_obj.search([("cost_type", "=", "labor")])
        for account in self:
            analytic_account_ids = account._get_all_analytic_accounts()
            account.revenue = self._get_journal_item_totals(
                revenue_journal_ids, analytic_account_ids
            )
            account.material_cost = -1 * self._get_journal_item_totals(
                material_journal_ids, analytic_account_ids
            )
            account.labor_cost = -1 * self._get_journal_item_totals(
                labor_journal_ids, analytic_account_ids
            )
        return True

    labor_cost = fields.Float(
        compute=compute_cost_revenue,
        string="Labor cost",
        digits="Account",
    )
    material_cost = fields.Float(
        compute=compute_cost_revenue,
        digits="Account",
    )
    total_cost = fields.Float(
        compute=compute_total_cost,
        digits="Account",
    )
    revenue = fields.Float(
        compute=compute_cost_revenue,
        digits="Account",
    )
    gross_profit = fields.Float(
        compute=compute_gross_profit,
        digits="Account",
    )
