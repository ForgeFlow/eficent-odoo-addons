# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestChanges(common.TransactionCase):

    def setUp(self):

        """***setup change tests***"""
        super(TestChanges, self).setUp()
        self.change_model = self.env['change.management.change']
        self.change_template_model = self.env['change.management.template']
        self.version_model = self.env['account.analytic.plan.version']
        self.project_model = self.env['project.project']
        self.product_model = self.env['product.product']
        self.anal_model = self.env['account.analytic.account']
        self.task_model = self.env['project.task']
        self.user_model = self.env['res.users']

        self.test_project = self.project_model.create(
            {'name': 'ChangeTestProject'})
        self.anal = self.test_project.analytic_account_id
        self.product_id = self.ref('product.product_product_4')
        self.product = self.product_model.browse(self.product_id)
        self.product.product_tmpl_id.revenue_analytic_plan_journal_id = \
            self.ref('analytic_plan.analytic_plan_journal_sale')
        self.version = self.version_model.search(
            [('default_plan', '=', True)])
        if not len(self.version):
            self.version = self.version_model.create(
                {'name': 'name',
                 'company_id': 1,
                 'default_plan': self.ref(
                     'analytic_plan.analytic_plan_version_P02'),
                 'active': True})
        self.template = self.change_template_model.create(
            {'name': 'name',
             'revenue_product_id': self.product_id,
             'version_id': self.version.id})
        self.test_change_id = self.change_model.create({
            'name': 'ChangeTest0001',
            'description': 'TestChange_SkyPaintBlue',
            'change_category_id': 1,
            'project_id': self.test_project.id,
            'change_value': '123.00',
            'change_template_id': self.template.id,
            'change_project_id': self.test_project.id})

    def test_change_owner_and_creator_added_to_followers_for_change(self):
        change = self.test_change_id
        change.set_state_active()
        change.set_state_accepted()
        self.assertEqual(
            self.anal.contract_value, 123.00, msg='wrong contract value'
        )
        change.set_state_draft()
        self.assertEqual(
            self.anal.contract_value, 00.00, msg='plan lines should be deleted'
        )
