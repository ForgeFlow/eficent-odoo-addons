# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
import time


class TestComputeWorkdays(TransactionCase):

    def setUp(self):
        super(TestComputeWorkdays, self).setUp()

        self.timesheet_sheet = self.env['hr_timesheet_sheet.sheet']
        self.project_2 = self.env.ref('project.project_project_2')
        self.dept = self.env.ref('hr.dep_management')
        self.dept_1 = self.env.ref('hr.dep_rd')
        self.root = self.env.ref('hr.employee_root')
        self.user = self.env.ref('base.user_root')
        self.root.write({'user_id': self.user.id})
        self.dept.write({
            'parent_id': self.dept_1.id,
            'manager_id': self.root.id
        })

        # create user
        user_dict = {
            'name': 'User 1',
            'login': 'tua@example.com',
            'password': 'base-test-passwd',
        }
        self.user_test = self.env['res.users'].create(user_dict)

        # create Employee
        employee_dict = {
            'name': 'Employee 1',
            'user_id': self.user_test.id,
            'address_id': self.user_test.partner_id.id,
            'parent_id': self.root.id,
        }
        self.employee = self.env['hr.employee'].create(employee_dict)

        self.timesheet_sheet = self.timesheet_sheet.create({
            'date_from': time.strftime('%Y-%m-11'),
            'date_to': time.strftime('%Y-%m-17'),
            'name': 'Employee 1',
            'state': 'new',
            'user_id': self.user_test.id,
            'employee_id': self.employee.id,
            'department_id': self.dept.id,
        })

        # I add 5 hours of work timesheet
        self.timesheet_sheet.write({'timesheet_ids': [(0, 0, {
            'project_id': self.project_2.id,
            'date': time.strftime('%Y-%m-11'),
            'name': 'Develop UT for hr module(1)',
            'user_id': self.user_test.id,
            'unit_amount': 5.00,
        })]})

    def test_timesheet_methods(self):
        self.timesheet_sheet.action_timesheet_confirm()
        self.assertEqual(self.timesheet_sheet.validator_user_ids,
                         self.timesheet_sheet.employee_id.parent_id.user_id)
        self.timesheet_sheet.action_timesheet_done()
        self.timesheet_sheet.action_timesheet_draft()
