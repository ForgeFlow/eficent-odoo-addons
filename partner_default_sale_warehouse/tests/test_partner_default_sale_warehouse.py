# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestPartnerDefaultSaleWarehouse(TransactionCase):

    def setUp(self):
        super(TestPartnerDefaultSaleWarehouse, self).setUp()
        self.sale_order_model = self.env['sale.order']
        self.partner_model = self.env['res.partner']
        self.warehouse_model = self.env['stock.warehouse']
        self.company_partner = self.env.ref('base.main_partner')

        self.wh1 = self.warehouse_model.create(
            {'partner_id': self.company_partner.id,
             'name': 'WH1',
             'code': 'WH1'})

        self.customer = self.partner_model.create(
            {'name': 'Partner1'})
        self.ship_to = self.partner_model.create(
            {'name': 'Ship-to for Partner 1',
             'parent_id': self.customer.id,
             'property_sale_warehouse_id': self.wh1.id}
        )
        self.product = self.env.ref('product.product_product_4')

    def test_sale_order_onchange_partner(self):
        sale_order = self.sale_order_model.new({'partner_shipping_id':
                                                    self.ship_to.id})
        sale_order._onchange_partner_shipping_id()

        self.assertEqual(sale_order.warehouse_id,
                         self.wh1,
                         'The sales order does not contain the default '
                         'warehouse indicated in the delivery address '
                         'partner.')