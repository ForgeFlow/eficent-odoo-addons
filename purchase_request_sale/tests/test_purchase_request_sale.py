# Copyright 2015-19 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestPurchaseRequestProcurement(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestPurchaseRequestProcurement, cls).setUpClass()
        cls.pr_model = cls.env['purchase.request']
        cls.prl_model = cls.env['purchase.request.line']
        cls.product_uom_model = cls.env['uom.uom']
        cls.supplierinfo_model = cls.env['product.supplierinfo']
        partner_values = {'name': 'Tupac'}
        cls.partner = cls.env['res.partner'].create(partner_values)
        partner_values = {'name': 'Todo a 100'}
        cls.partner_buy = cls.env['res.partner'].create(partner_values)
        cls.uom_unit_categ = cls.env.ref('uom.product_uom_categ_unit')
        product_values = {'name': 'Odoo',
                          'list_price': 5,
                          'type': 'product'}
        cls.product = cls.env['product.product'].create(product_values)
        cls.product_uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.product.route_ids = (
            cls.env.ref('stock.route_warehouse0_mto') |
            cls.env.ref('purchase_stock.route_warehouse0_buy')
        )
        for rule in cls.env.ref(
                'purchase_stock.route_warehouse0_buy').rule_ids:
            rule.propagate = True
            rule.group_propagation_option = 'propagate'
        supplierinfo_vals = {
            'name': cls.partner_buy.id,
            'product_tmpl_id': cls.product.product_tmpl_id.id,
            'price': 121.0
        }
        cls.supplierinfo_model.create(supplierinfo_vals)
        cls.product.product_tmpl_id.purchase_request = True

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
