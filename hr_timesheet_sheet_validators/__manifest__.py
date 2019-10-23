{
    "name": "HR Timesheet Sheet Validators",
    "version": "12.0.1.0.0",
    "author": "Eficent, Odoo Community Association (OCA)",
    "category": "Human Resources",
    "summary": """This module allows a user outside of the Human Resources
               groups to validate timesheets. A rule is predefined, but it
               is flexible enough to accept extensions.""",
    "website": "http://www.eficent.com",
    "license": "LGPL-3",
    "depends": ["hr_timesheet_sheet"],
    "data": [
        "security/hr_timesheet_sheet_security.xml",
        "views/hr_timesheet_sheet_view.xml",
    ],
    "installable": True,
}
