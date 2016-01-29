# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#               <contact@eficent.com>
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
    "name": "Work In Progress Statement including fiscal year totals",
    "version": "1.0",
    "author": "Eficent",
    "website": "",
    "category": "Generic Modules/Projects & Services",
    "depends": [
                "analytic_wip_report",
                ],
    "description": """
    """,

    "init_xml": [
                ],
    "update_xml": [
        "analytic_wip_report.xml",
        "account_analytic_account_view.xml",
        "wizards/analytic_wip_report_view.xml"
    ],
    'demo_xml': [

    ],
    'test':[
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}