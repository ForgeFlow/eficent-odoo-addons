# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestAnalyticCostRevenue(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestAnalyticCostRevenue, cls).setUpClass()
        cls.project_project = cls.env["project.project"]
        cls.project = cls.project_project.create(
            {"name": "Test project"}
        )
        cls.account_id = cls.project.analytic_account_id
        cls.product_simple = cls.env["product.product"].create(
            {"name": "xxx", "type": "product"}
        )
        cls.account_type = cls.env["account.account.type"].create(
            {"name": "Income", "type": "other"}
        )
        cls.analytic_journal_purchase = cls.env[
            "account.analytic.journal"
        ].create(
            {
                "name": "Purchase",
                "type": "purchase",
                "code": "PUR",
                "cost_type": "material",
            }
        )
        cls.analytic_journal_sale = cls.env["account.analytic.journal"].create(
            {
                "name": "Sale",
                "type": "sale",
                "code": "SAL",
                "cost_type": "revenue",
            }
        )
        cls.env["account.analytic.line"].create(
            {
                "product_id": cls.product_simple.id,
                "product_uom_id": cls.product_simple.uom_id.id,
                "name": "Simple",
                "date": "2020-02-01",
                "account_id": cls.account_id.id,
                "amount": -100,
                "unit_amount": 1.0,
                "journal_id": cls.analytic_journal_purchase.id,
            }
        )

        cls.env["account.analytic.line"].create(
            {
                "product_id": cls.product_simple.id,
                "product_uom_id": cls.product_simple.uom_id.id,
                "name": "Simple",
                "date": "2020-02-01",
                "account_id": cls.account_id.id,
                "amount": 200,
                "unit_amount": 1.0,
                "journal_id": cls.analytic_journal_sale.id,
            }
        )
        #  this checks it does not affect result
        cls.analytic_journal_no_cost = cls.env[
            "account.analytic.journal"
        ].create({"name": "Sale", "type": "sale", "code": "SAL"})
        cls.env["account.analytic.line"].create(
            {
                "product_id": cls.product_simple.id,
                "product_uom_id": cls.product_simple.uom_id.id,
                "name": "Simple",
                "date": "2020-02-01",
                "account_id": cls.account_id.id,
                "amount": 1.0,
                "unit_amount": 1.0,
                "journal_id": cls.analytic_journal_no_cost.id,
            }
        )

    def test_cost_revenue(self):
        self.assertEqual(self.account_id.material_cost, 100.0)
        self.assertEqual(self.account_id.labor_cost, 0.0)
        self.assertEqual(self.account_id.revenue, 200.0)
        self.assertEqual(self.account_id.gross_profit, 100.0)
