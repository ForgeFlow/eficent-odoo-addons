# -*- coding: utf8 -*-
#
# Copyright (C) 2014 NDP Systèmes (<http://www.ndp-systemes.fr>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from openerp.tests import common

class TestProductPutawayLast(common.TransactionCase):

    def setUp(self):
        super(TestProductPutawayLast, self).setUp()
        self.picking1 = self.browse_ref("product_putaway_last.picking_to_stock")
        self.move1 = self.browse_ref("product_putaway_last.move_to_stock")
        self.product_a1232 = self.browse_ref("product.product_product_6")
        self.location_shelf = self.browse_ref("stock.stock_location_components")
        self.location_stock = self.browse_ref("product_putaway_last.stock_location_stock")
        self.location_bin_1 = self.browse_ref("product_putaway_last.stock_location_bin_1")
        self.location_bin_2 = self.browse_ref("product_putaway_last.stock_location_bin_2")
        self.product_uom_unit_id = self.ref("product.product_uom_unit")


    def test_10_putaway_strategy(self):
        """Tests the correct operation of the last bin strategy."""
        self.picking1.action_confirm()
        self.picking1.action_assign()
        self.picking1.do_prepare_partial()
        self.picking1.do_transfer()
        self.assertEqual(self.picking1.state, 'done')
        quants_stock = self.env["stock.quant"].search([('product_id','=',self.product_a1232.id),
                                                       ('location_id','=',self.location_stock.id)])
        self.assertGreaterEqual(len(quants_stock), 1)
        quants_stock.in_date = "2015-01-15 16:23:45"
        move2 = self.env["stock.move"].create({
            'name': "Put in bin one",
            'product_id': self.product_a1232.id,
            'product_uom': self.product_uom_unit_id,
            'product_uom_qty': 15,
            'location_id': self.location_shelf.id,
            'location_dest_id': self.location_bin_1.id,
        })
        move2.action_confirm()
        move2.action_assign()
        move2.action_done()
        self.assertEqual(move2.state, 'done')
        quants_stock2 = self.env["stock.quant"].search([('product_id','=',self.product_a1232.id),
                                                       ('location_id','=',self.location_bin_1.id)])
        self.assertGreaterEqual(len(quants_stock2), 1)
        quants_stock2.in_date = "2015-01-15 16:23:47"
        picking2 = self.picking1.copy()
        picking2.action_confirm()
        picking2.action_assign()
        picking2.do_prepare_partial()
        picking2.do_transfer()
        self.assertEqual(picking2.state, 'done')
        quants_stock3 = self.env["stock.quant"].search([('product_id','=',self.product_a1232.id),
                                                       ('location_id','=',self.location_bin_1.id)])
        self.assertGreaterEqual(len(quants_stock3), 2)


