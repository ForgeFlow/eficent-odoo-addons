# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo import fields
from odoo.exceptions import ValidationError


class TestPurchaseOrderLine(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseOrderLine, self).setUp()
        self.PurchaseOrder = self.env["purchase.order"]
        self.AnalyticAccount = self.env["account.analytic.account"]
        self.product_id_1 = self.env.ref("product.product_product_8")
        self.partner_id_2 = self.env.ref("base.res_partner_2")
        self.partner_id = self.env.ref("base.res_partner_1")
        self.analytic_account = self.AnalyticAccount.create(
            {"name": "Test Analytic Account"}
        )
        self.location = self.env["stock.location"].create(
            {
                "name": "ACC",
                "usage": "internal",
                "analytic_account_id": self.analytic_account.id,
            }
        )
        self.analytic_account.write(
            {"location_id": self.location.id}
        )
        self.po_vals = {
            "partner_id": self.partner_id.id,
            "order_line": [
                (
                    0,
                    0,
                    {
                        "name": self.product_id_1.name,
                        "product_id": self.product_id_1.id,
                        "product_qty": 5.0,
                        "location_dest_id": self.location.id,
                        "picking_type_id": 1,
                        "product_uom": self.product_id_1.uom_po_id.id,
                        "price_unit": 500.0,
                        "account_analytic_id": self.analytic_account.id,
                        "date_planned": fields.Datetime.today(),
                    },
                )
            ],
        }
        self.location_no_anal = self.env["stock.location"].create(
            {"name": "NO ANAL", "usage": "internal"}
        )
        self.po_no_anal_vals = {
            "partner_id": self.partner_id.id,
            "order_line": [
                (
                    0,
                    0,
                    {
                        "name": self.product_id_1.name,
                        "product_id": self.product_id_1.id,
                        "product_qty": 5.0,
                        "location_dest_id": self.location_no_anal.id,
                        "picking_type_id": 1,
                        "product_uom": self.product_id_1.uom_po_id.id,
                        "price_unit": 500.0,
                        "account_analytic_id": self.analytic_account.id,
                        "date_planned": fields.Datetime.today(),
                    },
                )
            ],
        }

    def test_check_purchase_analytic(self):
        self.po = self.PurchaseOrder.create(self.po_vals)
        self.po.button_confirm()
        self.picking = self.po.picking_ids
        self.picking.action_assign()
        self.picking.button_validate()
        self.assertEqual(
            self.picking.location_dest_id.analytic_account_id,
            self.po.project_id,
        )

    def test_check_purchase_no_analytic(self):
        with self.assertRaises(ValidationError):
            self.po = self.PurchaseOrder.create(self.po_no_anal_vals)
