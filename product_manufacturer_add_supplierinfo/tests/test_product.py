# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestProduct(common.TransactionCase):

    def setUp(self):
        super(TestProduct, self).setUp()
        self.product_tmpl_model = self.env['product.template']
        self.tax_model = self.env['account.tax']
        self.supplierinfo_model = self.env["product.supplierinfo"]
        self.partner_id = self.env.ref('base.res_partner_2')
        self.partner_id_1 = self.env.ref('base.res_partner_3')
        supplierinfo = self.supplierinfo_model.create({
            'name': self.partner_id.id,
            'price': 121.0,
        })
        tax_include_id = self.tax_model.create({
            'name': "Include tax",
            'amount': 21.00,
            'price_include': True,
            'type_tax_use': 'purchase'
        })
        self.product_tmpl_id = self.product_tmpl_model.create({
            'name': "Voiture",
            'manufacturer': self.partner_id.id,
            'list_price': 121,
            'seller_ids': [(6, 0, [supplierinfo.id])],
            'supplier_taxes_id': [(6, 0, [tax_include_id.id])]
        })

    def test_method(self):
        self.product_tmpl_id.write({
            'manufacturer': self.partner_id_1.id
        })
        self.assertEqual(self.product_tmpl_id.seller_ids[0].name.id,
                         self.partner_id.id)
