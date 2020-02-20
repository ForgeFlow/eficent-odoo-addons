# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo import fields


class TestAnalyticCostRevenue(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestAnalyticCostRevenue, cls).setUpClass()
        cls.project_project = cls.env["project.project"]
        cls.project = cls.project_project.create(
            {"name": "Test project", "code": "ACV0001"}
        )
        cls.account_obj = cls.env["account.account"]
        cls.partner = cls.env.ref("base.res_partner_2")
        cls.product_id = cls.env.ref("product.consu_delivery_03")
        cls.analytic_line_plan_obj = cls.env["account.analytic.line.plan"]
        cls.account_id = cls.project.analytic_account_id
        cls.product_simple = cls.env["product.product"].create(
            {"name": "xxx", "type": "product"}
        )
        cls.expense = cls.env.ref("account.data_account_type_expenses").id
        cls.analytic_plan_version = cls.env.ref(
            "analytic_plan.analytic_plan_version_P02"
        )
        cls.general_account_id = cls.env["account.account"].search(
            [("user_type_id", "=", cls.expense)], limit=1
        )
        cls.account_type = cls.env["account.account.type"].create(
            {"name": "Income", "type": "other"}
        )
        cls.analytic_journal_purchase = cls.env[
            "account.analytic.plan.journal"
        ].create(
            {
                "name": "Purchase",
                "type": "purchase",
                "code": "PUR",
                "cost_type": "material",
            }
        )
        cls.analytic_journal_sale = cls.env[
            "account.analytic.plan.journal"
        ].create(
            {
                "name": "Sale",
                "type": "sale",
                "code": "SAL",
                "cost_type": "revenue",
            }
        )
        cls.analytic_line_plan = cls.analytic_line_plan_obj.create(
            {
                "name": cls.product_id.name,
                "date": fields.Date.today(),
                "amount": 100,
                "unit_amount": 10,
                "account_id": cls.account_id.id,
                "partner_id": cls.partner.id,
                "journal_id": cls.analytic_journal_purchase.id,
                "version_id": cls.analytic_plan_version.id,
                "product_id": cls.product_id.id,
                "general_account_id": cls.general_account_id.id,
            }
        )

        cls.analytic_line_plan = cls.analytic_line_plan_obj.create(
            {
                "name": cls.product_id.name,
                "date": fields.Date.today(),
                "amount": 200,
                "unit_amount": 10,
                "account_id": cls.account_id.id,
                "partner_id": cls.partner.id,
                "journal_id": cls.analytic_journal_sale.id,
                "version_id": cls.analytic_plan_version.id,
                "product_id": cls.product_id.id,
                "general_account_id": cls.general_account_id.id,
            }
        )

        #  this checks it does not affect result
        cls.analytic_journal_no_cost = cls.env[
            "account.analytic.plan.journal"
        ].create({"name": "Sale", "type": "sale", "code": "SAL"})
        cls.analytic_line_plan = cls.analytic_line_plan_obj.create(
            {
                "name": cls.product_id.name,
                "date": fields.Date.today(),
                "amount": 100,
                "unit_amount": 10,
                "account_id": cls.account_id.id,
                "partner_id": cls.partner.id,
                "journal_id": cls.analytic_journal_no_cost.id,
                "version_id": cls.analytic_plan_version.id,
                "product_id": cls.product_id.id,
                "general_account_id": cls.general_account_id.id,
            }
        )

    def test_cost_revenue(self):
        self.assertEqual(self.account_id.material_cost_plan, -100.0)
        self.assertEqual(self.account_id.labor_cost_plan, 0.0)
        self.assertEqual(self.account_id.revenue_plan, 200.0)
        self.assertEqual(self.account_id.gross_profit_plan, 100.0)
