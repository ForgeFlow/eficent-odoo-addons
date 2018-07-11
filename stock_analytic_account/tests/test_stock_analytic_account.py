# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services S.L.
# Copyright 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestStockAnalyticAccount(common.TransactionCase):

    def setUp(self):
        super(TestStockAnalyticAccount, self).setUp()
        self.AnalyticAccount = self.env['account.analytic.account']
        self.StockPicking = self.env['stock.picking']
        self.StockMove = self.env['stock.move']
        self.ProcurementOrder = self.env['procurement.order']
        self.route_warehouse0_mto_id =\
            self.env.ref('stock.route_warehouse0_mto').id
        self.partner_id = self.env.ref('base.res_partner_1')
        self.product_icecream = self.env.ref('stock.product_icecream')
        self.product_icecream.write({
            'route_ids': [(6, 0, [self.route_warehouse0_mto_id])],
        })
        self.analytic_account = self.env.ref('analytic.analytic_agrolait')
        self.warehouse = self.env.ref('stock.warehouse0')
        self.location = self.env['stock.location'].create(
            {'name': self.analytic_account.name,
             'analytic_account_id': self.analytic_account.id})
        self.dest_location = self.env.ref('stock.stock_location_customers')
        self.outgoing_picking_type = self.env.ref('stock.picking_type_out')

        product_qty = self.env['stock.change.product.qty'].create({
            'location_id': self.location.id,
            'product_id': self.product_icecream.id,
            'new_quantity': 20,
        })
        product_qty.change_product_qty()

        # create Picking
        picking_data = {
            'partner_id': self.partner_id.id,
            'picking_type_id': self.outgoing_picking_type.id,
            'move_type': 'direct',
            'location_id': self.location.id,
            'location_dest_id': self.dest_location.id,
        }
        self.picking = self.StockPicking.create(picking_data)

        # create move
        move_data = {
            'picking_id': self.picking.id,
            'product_id': self.product_icecream.id,
            'name': self.product_icecream.name,
            'product_uom_qty': 11.0,
            'product_uom': self.product_icecream.uom_id.id,
            'location_id': self.location.id,
            'location_dest_id': self.dest_location.id,
            'analytic_account_id': self.analytic_account.id
        }
        self.move = self.StockMove.create(move_data)

        self.picking.action_confirm()
        self.picking.action_assign()
        self.picking.action_done()

    def test_stock_analytic_account(self):
        """Test Procurement Order And Move"""
        self.analytic_account = self.AnalyticAccount.\
            search([('id', '=', self.move.analytic_account_id.id)])
        self.assertEqual(self.picking.analytic_account_ids,
                         self.move.analytic_account_id)
        self.assertEqual(self.move.analytic_account_id,
                         self.analytic_account.move_ids.analytic_account_id)
        self.assertEqual(
            self.move.quant_ids[1].analytic_account_id,
            self.analytic_account.move_ids.quant_ids[1].analytic_account_id)
