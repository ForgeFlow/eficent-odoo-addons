from odoo.tests.common import TransactionCase
import time


class TestHRTimesheetSheetImportAccounts(TransactionCase):
    def setUp(self):
        super(TestHRTimesheetSheetImportAccounts, self).setUp()

        self.timesheet_sheet = self.env["hr_timesheet.sheet"]
        self.analytic_line = self.env["account.analytic.line"]
        self.project_2 = self.env.ref("project.project_project_2")
        self.dept = self.env.ref("hr.dep_management")
        self.dept_1 = self.env.ref("hr.dep_rd")
        self.root = self.env.ref("hr.employee_admin")
        self.user = self.env.ref("base.user_admin")
        self.root.write({"user_id": self.user.id})
        self.dept.write(
            {"parent_id": self.dept_1.id, "manager_id": self.root.id}
        )
        self.product = self.env.ref("product.product_product_11")
        self.product.write({"is_employee": True})
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
            "product_id": self.product.id,
        }
        self.employee = self.env["hr.employee"].create(employee_dict)

        self.timesheet_sheet_1 = self._create_timesheet_sheet(
            time.strftime("%Y-%m-11"), time.strftime("%Y-%m-17"), qty=5
        )
        self.timesheet_sheet_2 = self._create_timesheet_sheet(
            time.strftime("%Y-%m-18"), time.strftime("%Y-%m-24"), qty=10
        )

    def _create_timesheet_sheet(self, date_start, date_end, qty):
        timesheet_sheet = self.timesheet_sheet.create(
            {
                "date_start": date_start,
                "date_end": date_end,
                "name": "Employee 1",
                "state": "new",
                "user_id": self.user_test.id,
                "employee_id": self.employee.id,
                "department_id": self.dept.id,
            }
        )

        # I add 5 hours of work timesheet
        timesheet_sheet.write(
            {
                "timesheet_ids": [
                    (
                        0,
                        0,
                        {
                            "project_id": self.project_2.id,
                            "date": date_start,
                            "name": "Develop UT for hr module(1)",
                            "user_id": self.user_test.id,
                            "unit_amount": qty,
                        },
                    )
                ]
            }
        )
        return timesheet_sheet

    def test_timesheet_methods(self):
        self.timesheet_sheet_1.action_timesheet_confirm()
        self.timesheet_sheet_2.set_previous_timesheet_ids()
        analytic_1 = self.timesheet_sheet_1.timesheet_ids.mapped("account_id")
        analytic_2 = self.timesheet_sheet_2.timesheet_ids.mapped("account_id")
        self.assertEqual(len(analytic_2), 1)
        self.assertEqual(analytic_1.id, analytic_2.id)
