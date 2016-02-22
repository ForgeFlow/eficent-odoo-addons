# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Analytic Stage Use Timesheets",
    "version": "7.0.1.0.0",
    "summary": "Defaults the Use Timesheets field depending on the stage of "
               "the project/analytic account",
    "author": "Eficent",
    "website": "http://www.eficent.com",
    "category": "Generic",
    "depends": ["project_wbs", "hr_timesheet"],
    "license": "AGPL-3",
    "data": [
        "views/analytic_account_stage_view.xml",
    ],
    'installable': True,
    'active': False,
}
