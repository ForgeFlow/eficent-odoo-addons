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
    "name": "Stock Analytic Account Reports",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    'summary': 'Adds the analytic account to stock moves',
    "depends": ["stock_analytic_account"],
    "description": """
Project Procurement
===================
Features of this module:
    - Adds reports
    """,
    "init_xml": [],
    'data': [
             'report/report_stock_analytic_account_view.xml',
             'report/report_stock_move_view.xml',
             'report/report_stock_view.xml',
             'security/ir.model.access.csv'
    ],
    'test': [
        'test/stock_users.yml',
        'demo/stock_demo.yml',
        'test/opening_stock.yml',
        'test/shipment.yml',
        'test/stock_report.yml',
        'test/setlast_tracking.yml',
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
