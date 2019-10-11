# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Luxim d.o.o.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Deneroteam.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.analytic_resource_plan.tests import \
    test_analytic_resource_plan


class TestAnalyticResourcePlanStock(
        test_analytic_resource_plan.TestAnalyticResourcePlan):

    def setUp(cls):
        super(TestAnalyticResourcePlanStock, cls).setUp()
        cls.location = cls.env['stock.location'].create({
            'name': 'ACC',
            'usage': 'internal',
            'parent_id': cls.env.ref('stock.stock_location_stock').id,
            'analytic_account_id': cls.account_id.id})
        cls.account_id.location_id = cls.location
        cls.account_id.picking_type_id = cls.env.ref('stock.picking_type_in')

    def test_res_stock(cls):
        cls.assertEqual(cls.resource_plan_line.qty_available, 0.0,
                        'Showing qty where there is not')
        cls.resource_plan_line.action_button_confirm()

        picking_in = cls.env['stock.picking'].create({
            'picking_type_id': cls.env.ref('stock.picking_type_in').id,
            'location_id': cls.env.ref('stock.stock_location_suppliers').id,
            'location_dest_id': cls.account_id.location_id.id})
        move1 = cls.env['stock.move'].create({
            'name': '/',
            'product_id': cls.resource_plan_line.product_id.id,
            'product_uom_qty': 5.0,
            'analytic_account_id': cls.account_id.id,
            'picking_id': picking_in.id,
            'procure_method': 'make_to_stock',
            'product_uom': cls.resource_plan_line.product_id.uom_id.id,
            'location_id': cls.env.ref('stock.stock_location_suppliers').id,
            'location_dest_id': cls.account_id.location_id.id,
        })
        picking_in.action_confirm()

        cls.resource_plan_line._compute_quantities()
        # recomputing here as no relation to the pickings in this module
        # to put in the api depends
        cls.assertEqual(cls.resource_plan_line.incoming_qty, 5.0,
                        'Bad Incoming Qty')
        cls.assertEqual(cls.resource_plan_line.virtual_available, 5.0,
                        'Bad virtual Qty')
        picking_in.button_validate()
        cls.assertEqual(cls.resource_plan_line.qty_available, 0.0,
                        'Bad QTY Available')
        picking_out = cls.env['stock.picking'].create({
            'picking_type_id': cls.env.ref('stock.picking_type_out').id,
            'location_id': cls.location.id,
            'location_dest_id': cls.env.ref(
                'stock.stock_location_customers').id})
        move1.move_line_ids.qty_done = 5.0
        picking_in.action_done()

        cls.env['stock.move'].create({
            'name': '/',
            'product_id': cls.resource_plan_line.product_id.id,
            'product_uom_qty': 4.0,
            'procure_method': 'make_to_stock',
            'analytic_account_id': cls.account_id.id,
            'picking_id': picking_out.id,
            'product_uom': cls.resource_plan_line.product_id.uom_id.id,
            'location_id': cls.location.id,
            'location_dest_id':
                cls.env.ref('stock.stock_location_customers').id,
        })
        picking_out.action_confirm()
        cls.resource_plan_line._compute_quantities()
        # recomputing here as no relation to the pickings in this module
        # to put in the api depends
        cls.assertEqual(cls.resource_plan_line.virtual_available, 1.0,
                        'Bad Virtually Qty available')
        cls.assertEqual(cls.resource_plan_line.outgoing_qty, 4.0,
                        'Bad Outgoing Qty')
