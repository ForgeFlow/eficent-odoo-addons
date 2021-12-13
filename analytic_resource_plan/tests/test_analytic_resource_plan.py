
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Luxim d.o.o.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Deneroteam.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestAnalyticResourcePlan(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestAnalyticResourcePlan, cls).setUpClass()
        cls.project = cls.env['project.project'].create(
            {'name': 'Test project',
             'code': 'XX0001'})
        cls.account_id = cls.project.analytic_account_id
        cls.plan_version = cls.env.ref(
            'analytic_plan.analytic_plan_version_P02')
        cls.plan_version.default_resource_plan = True
        cls.account_id.write({
            'active_analytic_planning_version': cls.plan_version.id})
        cls.product = cls.env['product.product'].create(
            {'name': 'SP', 'type': 'product'})
        cls.expense = cls.env.ref('account.data_account_type_expenses').id
        cls.general_account_id = cls.env['account.account'].\
            search([('user_type_id', '=', cls.expense)], limit=1)
        cls.product.categ_id.property_account_expense_categ_id = \
            cls.general_account_id
        cls.anal_journal = cls.env['account.analytic.journal'].create(
            {'name': 'Expenses',
             'code': 'EX',
             'type': 'purchase'}
        )
        cls.plan_expenses = cls.env['account.analytic.plan.journal'].create(
            {'name': 'expenses',
             'code': 'EXP',
             'analytic_journal': cls.anal_journal.id,
             }
        )
        cls.resource_plan_line = cls.env['analytic.resource.plan.line'].create(
            {'product_id': cls.product.id,
             'product_uom_id': cls.product.uom_id.id,
             'name': 'fetch',
             'account_id': cls.account_id.id,
             'unit_amount': 1.0,
             }
        )
        cls.product.write(
            {'expense_analytic_plan_journal_id': cls.plan_expenses.id,
             'property_account_expense_id': cls.general_account_id.id})

    def _create_account(self, acc_type, name, code, company):
        """Create an account."""
        account = self.account_model.create({
            'name': name,
            'code': code,
            'user_type_id': acc_type.id,
            'company_id': company.id
        })
        return account

    def test_plan(self):
        self.resource_plan_line.action_button_confirm()
        self.assertEqual(self.resource_plan_line.state, 'confirm')
        plan_line = self.env['account.analytic.line.plan'].search(
            [('resource_plan_id', '=', self.resource_plan_line.id)])
        self.assertEqual(len(plan_line), 1, 'Wrong plan lines number')
        self.resource_plan_line.action_button_draft()
        self.assertEqual(self.resource_plan_line.state, 'draft')
        plan_line = self.env['account.analytic.line.plan'].search(
            [('resource_plan_id', '=', self.resource_plan_line.id)])
        self.assertEqual(len(plan_line), 0, 'Plan line not deleted')
