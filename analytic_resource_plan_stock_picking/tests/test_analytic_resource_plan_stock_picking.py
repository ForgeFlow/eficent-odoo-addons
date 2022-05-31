# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import UserError
from odoo.addons.analytic_resource_plan_stock.tests import \
    test_analytic_resource_plan_stock


class TestAnalyticResourcePlanStockPicking(
        test_analytic_resource_plan_stock.TestAnalyticResourcePlanStock):
    def setUp(cls):
        super(TestAnalyticResourcePlanStockPicking, cls).setUp()
        cls.env.user.company_id.resource_auto_fetch = True
        cls.analytic_account_obj = cls.env['account.analytic.account']
        cls.resource_plan_line_obj =\
            cls.env['analytic.resource.plan.line']
        cls.mrp_bom_obj = cls.env['mrp.bom']
        cls.mrp_bom_line_obj = cls.env['mrp.bom.line']
        cls.product_id = cls.env.ref('product.product_product_27')
        cls.partner = cls.env.ref('base.res_partner_1')
        cls.analytic_plan_version =\
            cls.env.ref('analytic_plan.analytic_plan_version_P00')
        cls.location_id = cls.env.ref('stock.stock_location_stock')
        cls.product_id.write({'expense_analytic_plan_journal_id': 1})
        cls.analytic_plan_journal_obj =\
            cls.env['account.analytic.plan.journal']
        cls.purchase_request_obj = cls.env['purchase.request']
        cls.purchase_request_line_obj = cls.env['purchase.request.line']
        cls.partner = cls.env.ref('base.res_partner_1')
        cls.analytic_plan_version =\
            cls.env.ref('analytic_plan.analytic_plan_version_P00')
        cls.product_id = cls.env.ref('product.product_product_27')
        cls.location_id = cls.env.ref('stock.stock_location_stock')
        cls.analytic_plan_journal = cls.analytic_plan_journal_obj.create({
            'name': 'Sale',
            'type': 'sale',
            'code': 'SAL',
            'active': True
        })
        cls.product_id.write({
            'expense_analytic_plan_journal_id': cls.analytic_plan_journal.id
        })

    def test_analytic_resource_plan_stock_picking(cls):
        # error if no location
        with cls.assertRaises(UserError):
            cls.account_id.picking_type_id = False
            cls.resource_plan_line.action_button_confirm()
        cls.account_id.picking_type_id = cls.env.ref('stock.picking_type_in')
        cls.unit_amount = 2.0
        upd_qty = cls.env['stock.change.product.qty'].create({
            'product_id': cls.resource_plan_line.product_id.id,
            'product_tmpl_id': cls.resource_plan_line.product_id.
            product_tmpl_id.id,
            'new_quantity': 1.0,
            'location_id': cls.env.ref('stock.stock_location_stock').id
        })
        upd_qty.change_product_qty()
        cls.resource_plan_line.action_button_confirm()
        cls.assertEqual(
            cls.resource_plan_line.qty_fetched, 1.0, 'bad qty fetched')
