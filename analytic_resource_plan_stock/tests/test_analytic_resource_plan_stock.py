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

    @classmethod
    def setUpClass(cls):
        super(TestAnalyticResourcePlanStock, cls).setUpClass()
        cls.location = cls.env['stock.location'].create({
            'name': 'ACC',
            'usage': 'internal',
            'analytic_account_id': cls.account_id.id})
        cls.account_id.location_id = cls.location

    def test_res_stock(self):
        self.assertEqual(self.resource_plan_line.qty_available, 0.0,
                         'Showing qty where there is not')
        self.resource_plan_line.action_button_confirm()

        picking_in = self.env['stock.picking'].create({
            'picking_type_id': self.env.ref('stock.picking_type_in').id,
            'location_id': self.env.ref('stock.stock_location_suppliers').id,
            'location_dest_id': self.account_id.location_id.id})
        move1 = self.env['stock.move'].create({
            'name': '/',
            'product_id': self.resource_plan_line.product_id.id,
            'product_uom_qty': 5.0,
            'analytic_account_id': self.account_id.id,
            'picking_id': picking_in.id,
            'procure_method': 'make_to_stock',
            'product_uom': self.resource_plan_line.product_id.uom_id.id,
            'location_id': self.env.ref('stock.stock_location_suppliers').id,
            'location_dest_id': self.account_id.location_id.id,
        })
        picking_in.action_confirm()

        self.resource_plan_line._compute_quantities()
        # recomputing here as no relation to the pickings in this module
        # to put in the api depends
        self.assertEqual(self.resource_plan_line.incoming_qty, 5.0,
                         'Bad Incoming Qty')
        self.assertEqual(self.resource_plan_line.virtual_available, 5.0,
                         'Bad virtual Qty')
        picking_in.button_validate()
        self.assertEqual(self.resource_plan_line.qty_available, 0.0,
                         'Bad QTY Available')
        picking_out = self.env['stock.picking'].create({
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'location_id': self.location.id,
            'location_dest_id': self.env.ref(
                'stock.stock_location_customers').id})
        move1.move_line_ids.qty_done = 5.0
        picking_in.action_done()

        self.env['stock.move'].create({
            'name': '/',
            'product_id': self.resource_plan_line.product_id.id,
            'product_uom_qty': 4.0,
            'procure_method': 'make_to_stock',
            'analytic_account_id': self.account_id.id,
            'picking_id': picking_out.id,
            'product_uom': self.resource_plan_line.product_id.uom_id.id,
            'location_id': self.location.id,
            'location_dest_id':
                self.env.ref('stock.stock_location_customers').id,
        })
        picking_out.action_confirm()
        self.resource_plan_line._compute_quantities()
        # recomputing here as no relation to the pickings in this module
        # to put in the api depends
        self.assertEqual(self.resource_plan_line.virtual_available, 1.0,
                         'Bad Virtually Qty available')
        self.assertEqual(self.resource_plan_line.outgoing_qty, 4.0,
                         'Bad Outgoing Qty')
