# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#             <contact@eficent.com>
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
    "name": "Project Stock Move Link",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["project", "stock_analytic_account"],
    "description": """
Project Stock Move Link
=======================
Features of this module:
    - Adds button in the Project Form and an Action from Project's 'More'
    menu to list the Stock Moves associated to the selected project.

    """,
    "init_xml": [],
    "update_xml": [    
        "view/project_view.xml",
        "security/ir.model.access.csv",
        "security/stock_move_security.xml",
    ],
    'demo_xml': [],
    'test':[],
    'installable': True,
    'active': False,
    'certificate': '',
    'application': True,
}
