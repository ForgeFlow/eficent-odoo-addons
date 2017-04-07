# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Timesheet Sheet Validators',
    'version': '9.0.1.0.0',
    'author': 'Eficent',
    'category': 'Human Resources',
    'summary': "This module allows a user outside of the Human Resources "
               "groups to validate timesheets. A rule is predefined, but it "
               "is flexible enough to accept extensions.",
    'website': 'http://www.eficent.com',
    'depends': ['hr_timesheet_sheet'],
    'data': [
        # 'security/hr_timesheet_sheet_security.xml',
        'views/hr_timesheet_sheet_view.xml',
        'views/hr_timesheet_workflow.xml',
    ],
    'installable': True,
    'auto_install': False,
}
