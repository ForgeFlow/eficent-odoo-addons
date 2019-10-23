# Copyright 2014-17 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "HR Timesheet Sheet Import Accounts",
    "version": "12.0.1.0.1",
    "author": "Eficent, Odoo Community Association (OCA)",
    "category": "Human Resources",
    "summary": "This module lets the user import the analytic accounts from "
    "the previous timesheet, with a simple click.",
    "website": "http://www.eficent.com",
    "license": "LGPL-3",
    "depends": [
        "hr_timesheet_sheet",
        "hr_employee_product",
        "hr_timesheet_sheet_period",
    ],
    "data": [
        "views/hr_timesheet_sheet_view.xml",
        "views/hr_employee_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
