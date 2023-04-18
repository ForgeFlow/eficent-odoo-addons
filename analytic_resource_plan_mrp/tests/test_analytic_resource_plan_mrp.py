# Copyright 2015-17 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tools.safe_eval import safe_eval

from odoo.addons.analytic_resource_plan_stock.tests import (
    test_analytic_resource_plan_stock,
)


class TestAnalyticResourcePlanMrp(
    test_analytic_resource_plan_stock.TestAnalyticResourcePlanStock
):
    def setUp(self):
        super(TestAnalyticResourcePlanMrp, self).setUp()
        self.analytic_account_obj = self.env["account.analytic.account"]
        self.analytic_resource_plan_obj = self.env["analytic.resource.plan.line"]
        self.mrp_bom_obj = self.env["mrp.bom"]
        self.mrp_bom_line_obj = self.env["mrp.bom.line"]
        self.product_id = self.env.ref("product.product_product_27")
        self.partner = self.env.ref("base.res_partner_1")
        self.analytic_plan_version = self.env.ref(
            "analytic_plan.analytic_plan_version_P00"
        )
        self.location_id = self.env.ref("stock.stock_location_stock")
        self.product_id.write({"expense_analytic_plan_journal_id": 1})

        self.bom = self._create_bom(self.product_id)
        self.resource_plan_line_wbom_id = self._create_analytic_resource_plan(
            self.product_id
        )
        self.account_id.bom_id = self.bom.id

    def _create_bom(self, product):
        test_bom = self.mrp_bom_obj.create(
            {
                "product_id": product.id,
                "product_tmpl_id": product.product_tmpl_id.id,
                "product_uom_id": product.uom_id.id,
                "product_qty": 1.0,
                "type": "normal",
            }
        )
        self.mrp_bom_line_obj.create(
            {
                "bom_id": test_bom.id,
                "product_id": product.id,
                "product_qty": 2.0,
            }
        )
        return test_bom

    def _create_analytic_account(self, name, partner, analytic_plan_version, location):
        return self.analytic_account_obj.create(
            {
                "name": name,
                "partner_id": partner.id,
                "active_analytic_planning_version": analytic_plan_version.id,
                "location_id": location.id,
            }
        )

    def _create_analytic_resource_plan(self, product):
        return self.analytic_resource_plan_obj.create(
            {
                "name": product.name,
                "product_id": product.id,
                "unit_amount": 2.0,
                "product_uom_id": product.uom_id.id,
                "account_id": self.account_id.id,
                "resource_type": "procurement",
                "bom_id": self.bom.id,
            }
        )

    def test_resource_plan_line(self):
        self.resource_plan_line_wbom_id.action_button_confirm()
        child = self.resource_plan_line_wbom_id.child_ids
        plan_lines = self.env["account.analytic.line.plan"].search(
            [("resource_plan_id", "=", child.id)]
        )
        self.assertEqual(len(plan_lines), 1, "bad plan lines")
        self.assertEqual(child.state, "confirm", "child not confirm")
        self.assertEqual(child.unit_amount, 4.0, "wrong qty in child")
        # test produce
        wiz_id = (
            self.env["analytic.resource.plan.line.produce"]
            .with_context(
                active_model="analytic.resource.plan.line",
                active_ids=self.resource_plan_line_wbom_id.id,
            )
            .create({})
        )
        move_action = wiz_id.do_produce()
        move_id = safe_eval(move_action["domain"])[0][2]
        move = self.env["stock.move"].browse(move_id)[0]
        self.assertEqual(
            move.product_qty,
            self.resource_plan_line_wbom_id.unit_amount,
            "Wrong consumed qty",
        )
        # test consume
        wiz_id = (
            self.env["analytic.resource.plan.line.consume"]
            .with_context(
                active_model="analytic.resource.plan.line",
                active_ids=self.resource_plan_line_wbom_id.id,
            )
            .create({})
        )
        move_action = wiz_id.do_consume()
        move_id = safe_eval(move_action["domain"])[0][2]
        self.assertEqual(
            move.product_qty,
            self.resource_plan_line_wbom_id.unit_amount,
            "Wrong consumed qty",
        )
