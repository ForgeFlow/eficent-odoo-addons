# Copyright 2014-17 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "HR Timesheet Sheet Import Accounts",
    "version": "14.0.1.0.0",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "category": "Human Resources",
    "summary": "This module lets the user import the analytic accounts from "
    "the previous timesheet, with a simple click.",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "license": "AGPL-3",
    "depends": [
        "hr_timesheet_sheet",
        "hr_employee_product",
        "hr_timesheet_sheet_period",
        "hr_timesheet_cost_category",
    ],
    "data": [
        "views/hr_timesheet_sheet_view.xml",
        "views/hr_employee_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
