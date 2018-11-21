# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestStockLocationAnalyticMRP(TransactionCase):

    def setUp(self):
        super(TestStockLocationAnalyticMRP, self).setUp()
        # Get registries
        self.mrp_model = self.env["mrp.production"]
        self.location_model = self.env["stock.location"]
        self.analytic_model = self.env["account.analytic.account"]
        self.yourcompany_loc = self.env.ref('stock.stock_location_stock')
        self.company_id = self.env.ref('base.main_company')

        # Create Analytic Account
        self.AA1 = self.analytic_model.create({
            'name': 'AA1',
        })

        # Create Stock Location
        self.location1 = self.location_model.create({
            'name': self.AA1.name,
            'analytic_account_id': self.AA1.id,
            'company_id': False,
            'usage': 'internal'
        })
        self.category = self.env['product.category'].create({
            'name': 'Category for inventory',
            'type': 'normal',
        })
        self.product = self.env['product.product'].create({
            'name': 'Test product',
            'categ_id': self.category.id
        })
        self.bom = self.env['mrp.bom'].create(
            {
                'product_id': self.product.id,
                'product_tmpl_id': self.product.product_tmpl_id.id,
            })
        self.production = self.env['mrp.production'].create(
            {
                'product_id': self.product.id,
                'analytic_account_id': self.AA1.id,
                'location_src_id': self.location1.id,
                'location_dest_id': self.location1.id,
                'product_uom_id': self.product.uom_id.id,
                'bom_id': self.bom.id,
            })

    def test_mrp_stock_location_analytic(self):
        """Test MRP & Analytic in Location with assertRaises"""
        with self.assertRaises(ValidationError):
            self.production.write({
                'location_src_id': self.yourcompany_loc.id
            })
        with self.assertRaises(ValidationError):
            self.production.write({
                'location_dest_id':  self.yourcompany_loc.id
            })
        self.location1.write({'analytic_account_id': self.AA1.id})
        self.production.write({
            'location_src_id': self.location1.id,
            'location_dest_id': self.location1.id,
        })
        mrp = self.mrp_model.search(
            [('location_src_id.analytic_account_id', '=', self.AA1.id)])
        self.assertEqual(len(mrp), 1, 'No location in the production')
