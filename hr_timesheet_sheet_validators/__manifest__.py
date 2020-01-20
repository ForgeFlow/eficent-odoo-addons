# Copyright (C) 2017-20 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
{
    "name": "HR Timesheet Sheet Validators",
    "version": "12.0.1.1.0",
    "author": "ForgeFlow",
    "category": "Human Resources",
    "summary": """This module allows a user outside of the Human Resources
               groups to validate timesheets. A rule is predefined, but it
               is flexible enough to accept extensions.""",
    "website": "http://www.forgeflow.com",
    "license": "LGPL-3",
    "depends": ["hr_timesheet_sheet"],
    "data": [
        "security/hr_timesheet_sheet_security.xml",
        "views/hr_timesheet_sheet_view.xml",
        "views/res_config_settings_view.xml",
    ],
    "installable": True,
    'pre_init_hook': 'pre_init_hook',
}
