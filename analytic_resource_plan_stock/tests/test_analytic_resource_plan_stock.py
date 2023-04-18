# Copyright 2017 ForgeFlow S.L.
# Copyright 2017 Luxim d.o.o.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Deneroteam.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.analytic_resource_plan.tests import test_analytic_resource_plan


class TestAnalyticResourcePlanStock(
    test_analytic_resource_plan.TestAnalyticResourcePlan
):
    def setUp(self):
        super(TestAnalyticResourcePlanStock, self).setUp()
        self.location = (
            self.env["stock.location"]
            .with_context(skip_ou_check=True)
            .create(
                {
                    "name": "ACC",
                    "usage": "internal",
                    "analytic_account_id": self.account_id.id,
                }
            )
        )
        self.account_id.location_id = self.location
        self.account_id.picking_type_id = self.env.ref("stock.picking_type_in")

    def test_res_stock(self):
        self.assertEqual(
            self.resource_plan_line.qty_available, 0.0, "Showing qty where there is not"
        )
        self.resource_plan_line.action_button_confirm()

        picking_in = self.env["stock.picking"].create(
            {
                "picking_type_id": self.env.ref("stock.picking_type_in").id,
                "location_id": self.env.ref("stock.stock_location_suppliers").id,
                "location_dest_id": self.account_id.location_id.id,
            }
        )
        self.env["stock.move"].create(
            {
                "name": "/",
                "product_id": self.product.id,
                "product_uom_qty": 5.0,
                "analytic_account_id": self.account_id.id,
                "picking_id": picking_in.id,
                "product_uom": self.product.uom_id.id,
                "location_id": self.env.ref("stock.stock_location_suppliers").id,
                "location_dest_id": self.account_id.location_id.id,
            }
        )
        picking_in.action_confirm()
        # recomputing here as no relation to the pickings in this module
        # to put in the api depends
        self.assertEqual(self.resource_plan_line.incoming_qty, 5.0, "Bad Incoming Qty")
        self.assertEqual(
            self.resource_plan_line.virtual_available, 5.0, "Bad virtual Qty"
        )
        picking_in._action_done()
        self.assertEqual(
            self.resource_plan_line.qty_available, 5.0, "Bad QTY Available"
        )
        self.assertEqual(
            self.resource_plan_line.incoming_done_qty, 5.0, "Bad Incoming done Qty"
        )
        picking_out = self.env["stock.picking"].create(
            {
                "picking_type_id": self.env.ref("stock.picking_type_out").id,
                "location_id": self.location.id,
                "location_dest_id": self.account_id.location_id.id,
            }
        )
        self.env["stock.move"].create(
            {
                "name": "/",
                "product_id": self.product.id,
                "product_uom_qty": 4.0,
                "analytic_account_id": self.account_id.id,
                "picking_id": picking_out.id,
                "product_uom": self.product.uom_id.id,
                "location_id": self.location.id,
                "location_dest_id": self.env.ref("stock.stock_location_customers").id,
            }
        )
        picking_out.action_confirm()
        self.assertEqual(
            self.resource_plan_line.virtual_available, 1.0, "Bad Qty available"
        )
        self.assertEqual(
            self.resource_plan_line.outgoing_qty, 4.0, "Bad Incoming done Qty"
        )
        picking_out._action_done()
        self.assertEqual(
            self.resource_plan_line.outgoing_done_qty, 4.0, "Bad outgoing done Qty"
        )
