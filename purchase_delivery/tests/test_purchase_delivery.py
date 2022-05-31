# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime
from odoo.exceptions import ValidationError


class TestPurchaseDelivery(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseDelivery, self).setUp()
        self.PurchaseOrder = self.env['purchase.order']
        self.AnalyticAccount = self.env['account.analytic.account']
        self.product_id_1 = self.env.ref('product.product_product_8')
        self.partner_id_2 = self.env.ref('base.res_partner_2')
        self.partner_id = self.env.ref('base.res_partner_1')
        self.carrier_id = self.env.ref('delivery.delivery_carrier')
        self.carrier_id.write({
            'src_zip_from': 12345,
            'src_zip_to': 56890,
            'src_country_ids': [(6, 0, [self.env.user.country_id.id])],
            'src_state_ids': [(6, 0, [self.env.user.state_id.id])]
        })

        self.po_vals = {
            'partner_id': self.partner_id.id,
            'carrier_id': self.carrier_id.id,
            'order_line': [
                (0, 0, {
                    'name': self.product_id_1.name,
                    'product_id': self.product_id_1.id,
                    'product_qty': 5.0,
                    'product_uom': self.product_id_1.uom_po_id.id,
                    'price_unit': 500.0,
                    'date_planned': datetime.today().
                    strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                })],
        }
        self.po = self.PurchaseOrder.create(self.po_vals)

    def test_delivery(self):
        self.po.onchange_partner_id()
        self.carrier_id.with_context({'purchase_order_id': self.po.id
                                      }).get_price()
        self.carrier_id.name_get()
        self.po.delivery_set()
        self.po._compute_carrier_in_po()
        self.assertTrue(self.po.carrier_in_po)
