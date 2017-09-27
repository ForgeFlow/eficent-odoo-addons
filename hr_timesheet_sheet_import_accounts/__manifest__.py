# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Timesheet Sheet Import Accounts',
    'version': '10.0.1.0.0',
    'author': 'Eficent',
    'category': 'Human Resources',
    'summary': "This module lets the user import the analytic accounts from "
               "the previous timesheet, with a simple click.",
    'website': 'http://www.eficent.com',
    'depends': ['hr_timesheet_sheet'],
    'data': [
        'views/hr_timesheet_sheet_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}