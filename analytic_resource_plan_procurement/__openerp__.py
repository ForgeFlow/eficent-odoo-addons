# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
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
    "name": "Analytic Resource Planning - Procurement Orders",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["analytic_resource_plan", "analytic_location",
                "procurement_analytic", "analytic_resource_plan_stock"],
    "description": """
Analytic Resource Planning - Procurement Orders
===============================================
Module features:
    - Create procurement order from analytic resource planning lines

    """,
    "init_xml": [],
    "update_xml": [
        "wizard/analytic_resource_plan_line_make_procurement.xml",
        "views/procurement_order_view.xml",
        "views/analytic_resource_plan_view.xml",
    ],
    'demo_xml': [],
    'test':[],
    'installable': True,
    'active': False,
    'certificate': '',
}