# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo import fields


class TestAnalyticResourcePlanMrp(common.TransactionCase):
    def setUp(self):
        super(TestAnalyticResourcePlanMrp, self).setUp()

        self.analytic_account_obj = self.env['account.analytic.account']
        self.analytic_resource_plan_obj =\
            self.env['analytic.resource.plan.line']
        self.mrp_bom_obj = self.env['mrp.bom']
        self.mrp_bom_line_obj = self.env['mrp.bom.line']
        self.product_id = self.env.ref('product.product_product_27')
        self.partner = self.env.ref('base.res_partner_1')
        self.analytic_plan_version =\
            self.env.ref('analytic_plan.analytic_plan_version_P00')
        self.location_id = self.env.ref('stock.stock_location_stock')
        self.product_id.write({'expense_analytic_plan_journal_id': 1})

        self.mrp_bom = self._create_bom(self.product_id)
        self.analytic_account = self._create_analytic_account(
            'Test Analytic Account', self.partner, self.analytic_plan_version,
            self.location_id
        )

        self.analytic_resource_plan = self._create_analytic_resource_plan(
            self.product_id, self.analytic_account)

    def _create_bom(self, product):
        test_bom = self.mrp_bom_obj.create({
            'product_id': product.id,
            'product_tmpl_id': product.product_tmpl_id.id,
            'product_uom_id': product.uom_id.id,
            'product_qty': 4.0,
            'type': 'normal',
        })
        self.mrp_bom_line_obj.create({
            'bom_id': test_bom.id,
            'product_id': product.id,
            'product_qty': 2,
        })
        return test_bom

    def _create_analytic_account(self, name, partner, analytic_plan_version,
                                 location):
        return self.analytic_account_obj.create({
            'name': name,
            'partner_id': partner.id,
            'active_analytic_planning_version': analytic_plan_version.id,
            'location_id': location.id
        })

    def _create_analytic_resource_plan(self, product, analytic_account):
        return self.analytic_resource_plan_obj.create({
            'name': product.name,
            'product_id': product.id,
            'unit_amount': 10,
            'product_uom_id': product.uom_id.id,
            'account_id': analytic_account.id,
            'resource_type': 'procurement',
            'date': fields.Date.today(),
            'bom_id': self.mrp_bom.id,
        })

    def test_resource_plan_line(self):
        self.analytic_resource_plan.action_button_confirm()
        self.analytic_resource_plan.button_bom_explode_to_resource_plan()
