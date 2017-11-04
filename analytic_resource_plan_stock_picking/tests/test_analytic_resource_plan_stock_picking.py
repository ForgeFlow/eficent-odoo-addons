# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo import fields


class TestAnalyticResourcePlanStockPicking(TransactionCase):

    def setUp(self):
        super(TestAnalyticResourcePlanStockPicking, self).setUp()

        self.analytic_account_obj = self.env['account.analytic.account']
        self.analytic_resource_plan_obj =\
            self.env['analytic.resource.plan.line']
        self.analytic_plan_journal_obj =\
            self.env['account.analytic.plan.journal']
        self.purchase_request_obj = self.env['purchase.request']
        self.purchase_request_line_obj = self.env['purchase.request.line']
        self.partner = self.env.ref('base.res_partner_1')
        self.analytic_plan_version =\
            self.env.ref('analytic_plan.analytic_plan_version_P00')
        self.product_id = self.env.ref('product.product_product_27')
        self.location_id = self.env.ref('stock.stock_location_stock')

        self.analytic_plan_journal = self.analytic_plan_journal_obj.create({
            'name': 'Sale',
            'type': 'sale',
            'code': 'SAL',
            'active': True
        })
        self.product_id.write({
            'expense_analytic_plan_journal_id': self.analytic_plan_journal.id
        })
        self.analytic_account = self._create_analytic_account(
            'Test Analytic Account', self.partner,
            self.analytic_plan_version, None)
        self.analytic_account_1 = self._create_analytic_account(
            'Test Analytic Account 1', self.partner,
            self.analytic_plan_version, self.location_id.id)

        self.analytic_resource_plan = self._create_analytic_resource_plan(
            self.product_id, self.analytic_account)
        self.analytic_resource_plan_1 = self._create_analytic_resource_plan(
            self.product_id, self.analytic_account_1)

    def _create_analytic_account(self, name, partner, analytic_plan_version,
                                 location):
        return self.analytic_account_obj.create({
            'name': name,
            'partner_id': partner.id,
            'active_analytic_planning_version': analytic_plan_version.id,
            'location_id': location
        })

    def _create_analytic_resource_plan(self, product, analytic_account):
        return self.analytic_resource_plan_obj.create({
            'name': product.name,
            'product_id': product.id,
            'unit_amount': 10,
            'product_uom_id': product.uom_id.id,
            'account_id': analytic_account.id,
            'resource_type': 'procurement',
            'date': fields.Date.today()
        })

    def test_analytic_resource_plan_stock_picking(self):
        with self.assertRaises(UserError):
            self.analytic_resource_plan.action_button_confirm()
        self.analytic_resource_plan_1.action_button_confirm()
        self.purchase_request_line = self.purchase_request_line_obj.\
            search([('product_id', '=',
                     self.analytic_resource_plan_1.product_id.id),
                    ('analytic_account_id', '=',
                     self.analytic_resource_plan_1.account_id.id)])

        # check qty purchase request and analytic resource plan
        self.assertEqual(self.purchase_request_line.product_qty,
                         self.analytic_resource_plan_1.unit_amount)
        self.purchase_request = self.purchase_request_obj.\
            search([('line_ids', 'in', self.purchase_request_line.ids)])
        self.purchase_request.button_to_approve()
        self.purchase_request.button_approved()

        self.move = self.env['stock.move'].\
            search([('product_id', '=',
                     self.analytic_resource_plan_1.product_id.id),
                    ('analytic_account_id', '=',
                     self.analytic_resource_plan_1.account_id.id),
                    ('location_id', '=', self.location_id.id)])

        self.stock_picking = self.env['stock.picking'].\
            search([('analytic_resource_plan_line_id', '=',
                     self.analytic_resource_plan_1.id),
                    ('move_lines', 'in', self.move.ids)])

        # check picking analytic resource plan and analytic resource plan
        self.assertEqual(self.stock_picking.analytic_resource_plan_line_id,
                         self.analytic_resource_plan_1)
