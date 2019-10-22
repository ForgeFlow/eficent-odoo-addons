# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.analytic_resource_plan_stock.tests import (
    test_analytic_resource_plan_stock,
)
from odoo.tools.safe_eval import safe_eval


class TestAnalyticResourcePlanMrp(
    test_analytic_resource_plan_stock.TestAnalyticResourcePlanStock
):

    @classmethod
    def setUpClass(cls):
        super(TestAnalyticResourcePlanMrp, cls).setUpClass()
        cls.analytic_account_obj = cls.env["account.analytic.account"]
        cls.analytic_resource_plan_obj = cls.env["analytic.resource.plan.line"]
        cls.mrp_bom_obj = cls.env["mrp.bom"]
        cls.mrp_bom_line_obj = cls.env["mrp.bom.line"]
        cls.account_type = cls.env["account.account.type"].create(
            {"name": "Test account type", "type": "other"}
        )
        cls.gp_account_id = cls.env["account.account"].create(
            {
                "name": "Test account",
                "code": "TEST_ARP",
                "user_type_id": cls.account_type.id,
                "reconcile": True,
            }
        )
        cls.product_id = cls.env["product.product"].create({"name": "XXX"})
        cls.product.categ_id.property_account_expense_categ_id = (
            cls.gp_account_id
        )
        cls.partner = cls.env.ref("base.res_partner_1")
        cls.analytic_plan_version = cls.env.ref(
            "analytic_plan.analytic_plan_version_P00"
        )
        cls.location_id = cls.env.ref("stock.stock_location_stock")
        cls.product_id.write({"expense_analytic_plan_journal_id": 1})

        cls.bom = cls._create_bom(cls.product_id)
        cls.resource_plan_line_wbom_id = cls._create_analytic_resource_plan(
            cls.product_id)
        cls.account_id.bom_id = cls.bom.id

    @classmethod
    def _create_bom(cls, product):
        test_bom = cls.mrp_bom_obj.create(
            {
                "product_id": product.id,
                "product_tmpl_id": product.product_tmpl_id.id,
                "product_uom_id": product.uom_id.id,
                "product_qty": 1.0,
                "type": "normal",
            }
        )
        cls.mrp_bom_line_obj.create(
            {
                "bom_id": test_bom.id,
                "product_id": product.id,
                "product_qty": 2.0,
            }
        )
        return test_bom

    @classmethod
    def _create_analytic_account(
        cls, name, partner, analytic_plan_version, location
    ):
        return cls.analytic_account_obj.create(
            {
                "name": name,
                "partner_id": partner.id,
                "active_analytic_planning_version": analytic_plan_version.id,
                "location_id": location.id,
            }
        )

    @classmethod
    def _create_analytic_resource_plan(cls, product):
        return cls.analytic_resource_plan_obj.create(
            {
                "name": product.name,
                "product_id": product.id,
                "unit_amount": 2.0,
                "product_uom_id": product.uom_id.id,
                "account_id": cls.account_id.id,
                "resource_type": "procurement",
                "bom_id": cls.bom.id,
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
            move.product_qty, child.unit_amount, "Wrong consumed qty"
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
        wiz_id.do_consume()
        self.assertEqual(
            move.product_qty, child.unit_amount, "Wrong consumed qty"
        )
