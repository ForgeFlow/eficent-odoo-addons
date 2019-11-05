from datetime import datetime

from odoo.tests.common import TransactionCase


class TestPurchaseDelivery(TransactionCase):

    def setUp(self):
        super(TestPurchaseDelivery, self).setUp()
        self.PurchaseOrder = self.env["purchase.order"]
        self.AnalyticAccount = self.env["account.analytic.account"]
        self.product_id_1 = self.env.ref("product.product_product_8")
        self.partner_id_2 = self.env.ref("base.res_partner_2")
        self.partner_id = self.env.ref("base.res_partner_1")
        self.carrier_id = self.env.ref("delivery.delivery_carrier")
        self.carrier_id.write(
            {
                "src_zip_from": 12345,
                "src_zip_to": 56890,
                "src_country_ids": [(6, 0, [
                    x.id for x in self.env.user.country_id])],
                "src_state_ids": [(6, 0, [
                    x.id for x in self.env.user.state_id])],
            }
        )

        self.po_vals = {
            "partner_id": self.partner_id.id,
            "carrier_id": self.carrier_id.id,
            "order_line": [
                (
                    0,
                    0,
                    {
                        "name": self.product_id_1.name,
                        "product_id": self.product_id_1.id,
                        "product_qty": 5.0,
                        "product_uom": self.product_id_1.uom_po_id.id,
                        "price_unit": 500.0,
                        "date_planned": datetime.today(),
                    },
                )
            ],
        }
        self.po = self.PurchaseOrder.create(self.po_vals)

    def test_delivery(self):
        self.po.onchange_partner_id()
        self.po.button_confirm()
        self.picking = self.po.picking_ids
        self.picking.action_assign()
        self.picking.button_validate()
        self.assertTrue(self.picking.carrier_id)
        self.assertEqual(self.picking.carrier_id, self.po.carrier_id)
