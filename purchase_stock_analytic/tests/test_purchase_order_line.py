# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime
from odoo.exceptions import ValidationError


class TestPurchaseOrderLine(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseOrderLine, self).setUp()
        self.PurchaseOrder = self.env['purchase.order']
        self.AnalyticAccount = self.env['account.analytic.account']
        self.product_id_1 = self.env.ref('product.product_product_8')
        self.partner_id_2 = self.env.ref('base.res_partner_2')
        self.partner_id = self.env.ref('base.res_partner_1')
        self.analytic_account = self.AnalyticAccount.create({
            'name': 'Test Analytic Account',
        })
        self.location = self.env['stock.location'].create({
            'name': 'ACC',
            'usage': 'internal',
            'analytic_account_id': self.analytic_account.id})
        self.analytic_account.write({'location_id': self.location.id,
                                     'picking_type_id': 1})
        self.po_vals = {
            'partner_id': self.partner_id.id,
            'order_line': [
                (0, 0, {
                    'name': self.product_id_1.name,
                    'product_id': self.product_id_1.id,
                    'product_qty': 5.0,
                    'location_dest_id': self.location.id,
                    'picking_type_id': 1,
                    'product_uom': self.product_id_1.uom_po_id.id,
                    'price_unit': 500.0,
                    'account_analytic_id': self.analytic_account.id,
                    'date_planned': datetime.today().
                    strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                })],
        }
        self.location_no_anal = self.env['stock.location'].create({
            'name': 'NO ANAL',
            'usage': 'internal'})
        self.po_no_anal_vals = {
            'partner_id': self.partner_id.id,
            'order_line': [
                (0, 0, {
                    'name': self.product_id_1.name,
                    'product_id': self.product_id_1.id,
                    'product_qty': 5.0,
                    'location_dest_id': self.location_no_anal.id,
                    'picking_type_id': 1,
                    'product_uom': self.product_id_1.uom_po_id.id,
                    'price_unit': 500.0,
                    'account_analytic_id': self.analytic_account.id,
                    'date_planned': datetime.today().
                    strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                })],
        }

    def test_01_check_purchase_analytic(self):
        self.po = self.PurchaseOrder.create(self.po_vals)
        self.po.button_confirm()
        self.picking = self.po.picking_ids
        self.picking.force_assign()
        self.picking.do_new_transfer()
        self.assertEqual(
            self.picking.location_dest_id.analytic_account_id,
            self.po.project_id)

    def test_02_check_purchaseno_analytic(self):
        with self.assertRaises(ValidationError):
            self.po = self.PurchaseOrder.create(self.po_no_anal_vals)

    def test_03_check_purchase_analytic(self):
        """
        Test that if changed the analytic at parent level all the lines
        get the location of the project
        """
        po = self.PurchaseOrder.new(self.po_no_anal_vals)
        po.project_id = self.analytic_account
        po._onchange_project_id()  # in purchase_analytic_module
        po.onchange_analytic()  # in this module
        self.assertEqual(
            po.order_line.location_dest_id.analytic_account_id,
            po.project_id)
