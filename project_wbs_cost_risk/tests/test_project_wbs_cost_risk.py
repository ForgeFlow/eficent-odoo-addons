# -*- coding: utf-8 -*-
from odoo.tests import common
import time


class TestProjectAnalyticBudgetHours(common.TransactionCase):
    def setUp(self):
        super(TestProjectAnalyticBudgetHours, self).setUp()
        self.timeheet_model = self.env["hr_timesheet_sheet.sheet"]
        self.employee = self.env["hr.employee"].create({"name": "Dick"})
        self.project = self.env["project.project"].create(
            {"name": "Test project", "code": "0001"}
        )
        self.parent_account = self.project.analytic_account_id
        self.project_son = self.env["project.project"].create(
            {
                "name": "Test project son",
                "code": "01",
                "parent_id": self.parent_account.id,
            }
        )
        self.project_son2 = self.env["project.project"].create(
            {
                "name": "Test project son 2",
                "code": "02",
                "parent_id": self.parent_account.id,
            }
        )
        self.son_account = self.project_son.analytic_account_id
        self.project_grand_son = self.env["project.project"].create(
            {
                "name": "Test project grand son",
                "code": "001",
                "parent_id": self.son_account.id,
            }
        )
        self.grand_son_account = self.project_grand_son.analytic_account_id
        self.g_account_user = self.env.ref("account.group_account_user")
        self.user1 = self.env["res.users"].create(
            {
                "name": "Dick",
                "login": "iamdick",
                "password": "dickpwd",
                "email": "example@yourcompany.com",
                "company_id": self.env.user.company_id.id,
                "company_ids": [(4, self.env.user.company_id.id)],
                "groups_id": [(6, 0, self.g_account_user.ids)],
            }
        )
        self.employee.user_id = self.user1

    def test_01_budget_hours(self):
        "Test budget hours propagation"
        self.project_grand_son.budget_hours = 5.0
        self.project_son2.budget_hours = 2.0
        self.assertEquals(self.project_son.budget_hours, 5.0)
        self.assertEquals(self.project.budget_hours, 7.0)

    def test_02_actual_hours(self):
        "Test hours computation"
        timesheet_sheet = self.timeheet_model.create(
            {
                "employee_id": self.employee.id,
                "state": "new",
                "date_from": time.strftime("1990-01-01"),
                "date_to": time.strftime("1990-01-31"),
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
                            "project_id": self.project_grand_son.id,
                            "date": time.strftime("1990-01-02"),
                            "name": "hard work",
                            "user_id": self.user1.id,
                            "unit_amount": 5.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "project_id": self.project_son2.id,
                            "date": time.strftime("1990-01-03"),
                            "name": "hard work again",
                            "user_id": self.user1.id,
                            "unit_amount": 2.0,
                        },
                    ),
                ]
            }
        )
        # create aside analytic lines to confuse the system
        self.env["account.analytic.line"].create(
            {
                "name": "Test Line",
                "project_id": self.project_grand_son.id,
                "unit_amount": 1.0,
                "user_id": self.user1.id,
            }
        )
        self.env["account.analytic.line"].create(
            {
                "name": "Test Line 2",
                "project_id": self.project_son2.id,
                "unit_amount": 2.0,
                "user_id": self.user1.id,
            }
        )
        self.parent_account.budget_hours = 7
        self.project_son.analytic_account_id._compute_actual_project_hours()
        self.assertEquals(self.project_son.actual_hours, 5.0)
        self.project.analytic_account_id._compute_actual_project_hours()
        self.assertEquals(self.project.actual_hours, 7.0)
        self.project.analytic_account_id._compute_budget_hours_percentage()
        self.assertEquals(self.project.analytic_account_id.budget_hours_percentage, 100)
        self.project.analytic_account_id.is_cost_controlled = True
        self.project.analytic_account_id._compute_cost_alert_color()
        self.assertEquals(self.project.analytic_account_id.cost_alert_color, 3)
