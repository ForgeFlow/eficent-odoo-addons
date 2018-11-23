# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo.tests import common


class TestPurchaseRequestProcurement(common.SavepointCase):

    def setUp(self):
        super(TestPurchaseRequestProcurement, self).setUp()
        self.pr_model = self.env['purchase.request']
        self.prl_model = self.env['purchase.request.line']
        self.product_uom_model = self.env['product.uom']
        self.supplierinfo_model = self.env['product.supplierinfo']
        partner_values = {'name': 'Tupac'}
        self.partner = self.env['res.partner'].create(partner_values)
        partner_values = {'name': 'Todo a 100'}
        self.partner_buy = self.env['res.partner'].create(partner_values)
        self.uom_unit_categ = self.env.ref('product.product_uom_categ_unit')
        product_values = {'name': 'Odoo',
                          'list_price': 5,
                          'type': 'product'}
        self.product = self.env['product.product'].create(product_values)
        self.product_uom_unit = self.env.ref('product.product_uom_unit')
        self.product.route_ids = (
            self.env.ref('stock.route_warehouse0_mto') |
            self.env.ref('purchase.route_warehouse0_buy')
        )
        supplierinfo_vals = {
            'name': self.partner_buy.id,
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'price': 121.0
        }
        self.supplierinfo_model.create(supplierinfo_vals)
        self.product.product_tmpl_id.purchase_request = True

    def create_sale_order(self):
        sale_obj = self.env['sale.order']
        values = {
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_uom': self.product_uom_unit.id,
                'price_unit': 234.0,
                'product_uom_qty': 1})],
        }
        return sale_obj.create(values)

    def test_propagate(self):
        sale = self.create_sale_order()
        sale.action_confirm()
        self.assertEqual(len(sale.purchase_request_ids), 1, 'No link')
        sale.action_cancel()
        self.assertEqual(
            sale.purchase_request_ids[0].state, 'rejected', 'not rejected')
