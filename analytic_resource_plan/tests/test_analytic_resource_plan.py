# Copyright 2017 ForgeFlow S.L.
# Copyright 2017 Luxim d.o.o.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Deneroteam.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestAnalyticResourcePlan(TransactionCase):
    def setUp(self):
        super(TestAnalyticResourcePlan, self).setUp()
        next_id = (
            self.env["account.analytic.account"].search([], order="id desc", limit=1).id
            + 1
        )
        self.project = (
            self.env["project.project"]
            .with_context(skip_ou_check=True)
            .create({"name": "Test project", "code": "XX0 %s" % next_id})
        )
        self.account_id = self.project.analytic_account_id
        self.plan_version = self.env.ref("analytic_plan.analytic_plan_version_P02")
        self.plan_version.default_resource_plan = True
        self.account_id.write(
            {"active_analytic_planning_version": self.plan_version.id}
        )
        self.product = self.env["product.product"].create({"name": "SP"})
        self.anal_journal = self.env["account.analytic.journal"].create(
            {"name": "Expenses", "code": "EX", "type": "purchase"}
        )
        self.plan_expenses = self.env["account.analytic.plan.journal"].create(
            {
                "name": "expenses",
                "code": "EXP",
                "analytic_journal": self.anal_journal.id,
            }
        )
        self.resource_plan_line = self.env["analytic.resource.plan.line"].create(
            {
                "product_id": self.product.id,
                "product_uom_id": self.product.uom_id.id,
                "name": "fetch",
                "account_id": self.account_id.id,
                "unit_amount": 1.0,
            }
        )
        self.product.write(
            {
                "expense_analytic_plan_journal_id": self.plan_expenses.id,
            }
        )

    def test_plan(self):
        self.resource_plan_line.action_button_confirm()
        self.assertEqual(self.resource_plan_line.state, "confirm")
        plan_line = self.env["account.analytic.line.plan"].search(
            [("resource_plan_id", "=", self.resource_plan_line.id)]
        )
        self.assertEqual(len(plan_line), 1, "Wrong plan lines number")
        self.resource_plan_line.action_button_draft()
        self.assertEqual(self.resource_plan_line.state, "draft")
        plan_line = self.env["account.analytic.line.plan"].search(
            [("resource_plan_id", "=", self.resource_plan_line.id)]
        )
        self.assertEqual(len(plan_line), 0, "Plan line not deleted")
