# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
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
    "name": "Stock Analytic Account",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    'summary': 'Adds the analytic account to stock moves',
    "depends": ["stock", "analytic"],
    "description": """
Project Procurement
===================
Features of this module:
    - Adds the analytic account to the stock move
    - Makes it possible to search stock moves by analytic account or its project manager
    - Makes it possible to search picking lists by analytic account or its project manager
    - Adds button in the Project Form and an Action from Project's 'More' menu to list the
    Procurement Orders associated to the selected project.
    """,
    "init_xml": [],
    'data': [
             'view/stock_view.xml',
             'view/stock_picking_view.xml',
             'view/analytic_account_view.xml'
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
