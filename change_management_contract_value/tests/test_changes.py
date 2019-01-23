# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Enterprise Management Solution
#
#    Copyright (C) 2015 Matmoz d.o.o. (<http://www.matmoz.si>).
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


class TestChanges(common.TransactionCase):

    def setUp(self):

        """***setup change tests***"""
        super(TestChanges, self).setUp()
        cr, uid, = self.cr, self.uid

        self.change_model = self.registry('change.management.change')
        self.change_template_model = self.registry('change.management.template')
        self.version_model = self.registry('account.analytic.plan.version')
        self.project_model = self.registry('project.project')
        self.product_model = self.registry('product.product')
        self.anal_model = self.registry('account.analytic.account')
        self.task_model = self.registry('project.task')
        self.user_model = self.registry('res.users')

        self.test_project_id = self.project_model.create(
            cr, uid, {'name': 'ChangeTestProject'}
        )
        self.test_project = self.project_model.browse(
            cr, uid, self.test_project_id)
        self.anal = self.test_project.analytic_account_id
        self.product_id = self.ref('product.product_product_4')
        self.product = self.product_model.browse(cr, uid, self.product_id)
        self.product.product_tmpl_id.revenue_analytic_plan_journal_id = self.ref('analytic_plan.analytic_plan_journal_sale')
        self.version_id = self.version_model.create(
            cr, uid, {
                'name': 'name',
                'company_id': 1,
                'default_plan': self.ref('analytic_plan.analytic_plan_version_P02'),
                'active': True,
            }
        )
        self.template_id = self.change_template_model.create(
            cr, uid, {
                'name': 'name',
                'revenue_product_id': self.product_id,
                'version_id': self.version_id,
            }
        )
        self.test_change_id = self.change_model.create(
            cr, uid, {
                'name': 'ChangeTest0001',
                'description': 'TestChange_SkyPaintBlue',
                'change_category_id': 1,
                'project_id': self.test_project_id,
                'change_value': '123.00',
                'change_template_id': self.template_id,
                'change_project_id': self.test_project_id,
            }
        )

    def test_change_owner_and_creator_added_to_followers_for_change(self):
        cr, uid = self.cr, self.uid
        change = self.change_model.browse(cr, uid, self.test_change_id)
        change.set_state_active(cr, uid)
        change.set_state_accepted(cr, uid)
        self.assertEqual(
            self.anal.contract_value, 123.00, msg='wrong contract value'
        )
        change.set_state_draft(cr, uid)
        self.assertEqual(
            self.anal.contract_value, 00.00, msg='plan lines should be deleted'
        )
