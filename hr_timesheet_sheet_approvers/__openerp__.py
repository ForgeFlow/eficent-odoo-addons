# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              Eficent <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Timesheet approvers',
    'version': '1.0',
    'author': 'Eficent',
    'category': 'Human Resources',
    'description': """
Timesheet approvers.
========================================

It is frequent for companies to restrict the visibility of
timesheets only to certain employees.

The current functionality allows any user in groups:
* 'Human Resources / Officer'
* 'Human Resources / Manager'
, to list and approve any timesheet.

This module incorporates the following features:

    Adds an additional layer of security for users in group
    'Human Resources / Officer', to allow only to approve timesheets to
    the manager of the department to which the employee is assigned,
    or to the employee's manager.

    Adds filters on timesheets to approve "My department's" and "My employees",
    that will show only  the timesheets that are associated to the department's
    or employee manager respectively. As a consequence, even users in group
    'Human Resources / Manager' will be able to list all employee's timesheets, but
    at the same time will know which timesheets they should approve.ç

    Adds the deparment and employee's manager to the timesheet form and
    list views.

    Shows the department of the employee, in the form and tree views.

    When the timesheet is confirmed, the manager of the department is
    added as a follower.

    """,
    'website': 'http://www.eficent.com',
    'depends': ['hr_timesheet_sheet'],
    'data': [
        'security/hr_timesheet_sheet_security.xml',
        'view/hr_timesheet_sheet_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}