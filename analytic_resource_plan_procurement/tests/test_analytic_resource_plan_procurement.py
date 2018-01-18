# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2018 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.tests import common
from openerp.tools.safe_eval import safe_eval as eval


class TestAnalyticResourcePlanProcurement(common.TransactionCase):

    def setUp(self):

        """***setup change tests***"""
        super(TestAnalyticResourcePlanProcurement, self).setUp()
        cr, uid = self.cr, self.uid
        self.analytic_account_obj = self.registry('account.analytic.account')
        self.analytic_resource_plan_obj =\
            self.registry('analytic.resource.plan.line')
        self.ARP_procument_obj =\
            self.registry('analytic.resource.plan.line.make.procurement')
        self.procurement_obj = self.registry('procurement.order')
        self.product = self.ref('product.product_product_27')
        self.partner = self.ref('base.res_partner_1')
        self.analytic_plan_version =\
            self.ref('analytic_plan.analytic_plan_version_P00')
        self.analytic_plan_version =\
            self.registry('account.analytic.plan.version'
                          ).browse(cr, uid, self.analytic_plan_version)
        self.analytic_plan_version.write({'default_resource_plan': True})
        self.location_id = self.ref('stock.stock_location_stock')
        self.product_id = self.registry('product.product'
                                        ).browse(cr, uid, self.product)
        self.product_id.write({'expense_analytic_plan_journal_id': 1})

        self.analytic_account = self._create_analytic_account(
            cr, uid, 'Test Analytic Account', self.partner,
            self.analytic_plan_version.id, self.location_id
        )

        self.analytic_resource_plan = self._create_analytic_resource_plan(
            cr, uid, self.product_id, self.analytic_account
        )

    def _create_analytic_account(self, cr, uid, name, partner,
                                 analytic_plan_version, location):
        return self.analytic_account_obj.create(cr, uid, {
            'name': name,
            'partner_id': partner,
            'active_analytic_planning_version': analytic_plan_version,
            'location_id': location,
        })

    def _create_analytic_resource_plan(self, cr, uid, product,
                                       analytic_account):
        return self.analytic_resource_plan_obj.create(cr, uid, {
            'name': product.name,
            'product_id': product.id,
            'unit_amount': 10,
            'product_uom_id': product.uom_id.id,
            'account_id': analytic_account,
            'resource_type': 'procurement',
            'date': '2017/02/07',
        })

    def test_change_owner_and_creator_added_to_followers_for_change(self):
        cr, uid, context = self.cr, self.uid, {}
        self.analytic_resource_plan = self.analytic_resource_plan_obj.\
            browse(cr, uid, self.analytic_resource_plan)

        wiz_context = {
            'active_ids': [self.analytic_resource_plan.id],
            'active_model': 'analytic.resource.plan.line',
            'active_id': 1
        }
        self.ARP_procument = self.ARP_procument_obj.create(cr, uid, {
            'direct_ship': False,
            'procure_method': 'make_to_order',
            'item_ids': [(0, 0, {'line_id': self.analytic_resource_plan.id,
                                 'product_qty': 10
                                 })]
        }, context=wiz_context)
        self.ARP_procument = self.ARP_procument_obj.browse(cr, uid,
                                                           self.ARP_procument)

        self.analytic_resource_plan.action_button_confirm()
        wizard = self.ARP_procument.make_procurement()
        domain = eval(wizard['domain'])
        procurement = self.procurement_obj.browse(cr, uid, [domain[0][2][0]],
                                                  context=context)
        self.assertEqual(procurement[0].analytic_resource_plan_lines[0],
                         self.analytic_resource_plan)
        self.assertEqual(self.analytic_resource_plan.procurement_orders[0],
                         procurement[0])
