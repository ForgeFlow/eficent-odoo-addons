# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DT


class TestPurchaseLastPrice(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseLastPrice, self).setUp()
        self.purchase_model = self.env['purchase.order']
        self.purchase_line_model = self.env['purchase.order.line']
        self.location = self.env.ref('stock.stock_location_suppliers')
        self.sale_order_model = self.env['sale.order']
        self.sale_line_model = self.env['sale.order.line']
        self.pricelist = self.env.ref('product.list0')
        partner_values = {'name': 'Peace and love'}
        self.partner = self.env['res.partner'].create(partner_values)
        self.partner_p = self.env.ref('base.res_partner_1')
        product_values = {'name': 'Gun',
                          'list_price': 5,
                          'type': 'product'}
        self.product = self.env['product.product'].create(product_values)
        self.product_uom_unit = self.env.ref('product.product_uom_unit')

    def create_sale_order(self):
        sale_obj = self.env['sale.order']
        values = {
            'partner_id': self.partner.id,
            'commitment_date': '02-02-2010',
            'order_line': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_uom': self.product_uom_unit.id,
                'price_unit': 234.0,
                'product_uom_qty': 1})],
        }
        return sale_obj.create(values)

    def test_purchase_last_price(self):
        purchase_order = self.purchase_model.create({
            'partner_id': self.partner_p.id,
            'location_id': self.location.id,
            'pricelist_id': self.pricelist.id,
            'date': '01-01-2010',
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'price_unit': 123.0,
                'product_uom': self.env.ref('product.product_uom_unit').id,
                'product_qty': 5.0,
                'name': self.product.name,
                'date_planned': '01-01-2010'
            })]
        })
        purchase_order.button_confirm()
        sale = self.create_sale_order()
        sale.order_line._get_last_purchase()
        p_date = datetime.strptime(purchase_order.date_order, DT)
        p_date = p_date.date().strftime(DF)
        for line in sale.order_line:
            self.assertEqual(line.last_supplier_id.id, self.partner_p.id)
            self.assertEqual(line.last_purchase_price, 123.0)
            self.assertEqual(line.last_purchase_date, p_date)
