# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from itertools import chain


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

    @api.multi
    def _get_all_analytic_accounts(self):
        # Now add the children
        query = """
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
        """
        # pylint: disable=sql-injection
        query = query.format(id1=", ".join([str(i) for i in self._ids]))
        self.env.cr.execute(query)
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
    def compute_total_cost(self):
        for account in self:
            account.total_cost = account.material_cost + account.labor_cost
        return True

    @api.multi
    def compute_gross_profit(self):
        for account in self:
            account.gross_profit = account.revenue - account.total_cost
        return True

    @api.multi
    def compute_cost_revenue(self):
        journal_obj = self.env["account.analytic.journal"]
        material_journal_ids = journal_obj.search(
            [("cost_type", "=", "material")]
        )
        revenue_journal_ids = journal_obj.search(
            [("cost_type", "=", "revenue")]
        )
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
        digits=dp.get_precision("Account"),
    )
    material_cost = fields.Float(
        compute=compute_cost_revenue,
        string="Material cost",
        digits=dp.get_precision("Account"),
    )
    total_cost = fields.Float(
        compute=compute_total_cost,
        string="Total cost",
        digits=dp.get_precision("Account"),
    )
    revenue = fields.Float(
        compute=compute_cost_revenue,
        string="Revenue",
        digits=dp.get_precision("Account"),
    )
    gross_profit = fields.Float(
        compute=compute_gross_profit,
        string="Gross Profit",
        digits=dp.get_precision("Account"),
    )
