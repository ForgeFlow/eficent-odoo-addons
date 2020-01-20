from odoo.tests.common import TransactionCase
import time
from odoo.exceptions import UserError


class TestComputeWorkdays(TransactionCase):
    def setUp(self):
        super(TestComputeWorkdays, self).setUp()

        self.timesheet_sheet = self.env["hr_timesheet.sheet"]
        self.project_2 = self.env.ref("project.project_project_2")
        self.dept = self.env.ref("hr.dep_management")
        self.dept_1 = self.env.ref("hr.dep_rd")
        self.root = self.env.ref("hr.employee_admin")
        self.user = self.env.ref("base.user_admin")
        # activate validators
        self.user.company_id.use_timesheet_validators = True
        self.root.write({"user_id": self.user.id})
        self.dept.write(
            {"parent_id": self.dept_1.id, "manager_id": self.root.id}
        )

        # create user
        user_dict = {
            "name": "User 1",
            "login": "tua@example.com",
            "password": "base-test-passwd",
        }
        self.user_test = self.env["res.users"].create(user_dict)

        # create Employee
        employee_dict = {
            "name": "Employee 1",
            "user_id": self.user_test.id,
            "address_id": self.user_test.partner_id.id,
            "parent_id": self.root.id,
        }
        self.employee = self.env["hr.employee"].create(employee_dict)

        self.timesheet_sheet = self.timesheet_sheet.create(
            {
                "date_start": time.strftime("%Y-%m-11"),
                "date_end": time.strftime("%Y-%m-17"),
                "name": "Employee 1",
                "state": "new",
                "user_id": self.user_test.id,
                "employee_id": self.employee.id,
                "department_id": self.dept.id,
            }
        )

        # I add 5 hours of work timesheet
        self.timesheet_sheet.write(
            {
                "timesheet_ids": [
                    (
                        0,
                        0,
                        {
                            "project_id": self.project_2.id,
                            "date": time.strftime("%Y-%m-11"),
                            "name": "Develop UT for hr module(1)",
                            "user_id": self.user_test.id,
                            "unit_amount": 5.00,
                        },
                    )
                ]
            }
        )

    def test_timesheet_methods(self):
        self.timesheet_sheet.action_timesheet_confirm()
        self.assertIn(
            self.timesheet_sheet.employee_id.parent_id.user_id,
            self.timesheet_sheet.validator_user_ids,
        )
        with self.assertRaises(UserError):
            self.timesheet_sheet.action_timesheet_done()
        self.timesheet_sheet.sudo(
            self.timesheet_sheet.employee_id.parent_id.user_id
        ).action_timesheet_done()
        with self.assertRaises(UserError):
            self.timesheet_sheet.sudo(
                self.timesheet_sheet.employee_id.user_id
            ).action_timesheet_draft()
        self.timesheet_sheet.sudo(
            self.timesheet_sheet.employee_id.parent_id.user_id
        ).action_timesheet_draft()
