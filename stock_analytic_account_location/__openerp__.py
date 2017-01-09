# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Stock Analytic Account Location',
    'version': '7.0.1.0.0',
    'category': 'Logistics',
    'summary': 'Stock analytic account using analytic locations',
    'description': """
    The move can only contain the analytic account if we are moving products
    in or out of the company. When the location is out of the company and
    contains and analytic account then the products are consumed for that
    project.
""",
    'author': 'Eficent',
    'website': 'http://www.eficent.com',
    'depends': ['stock', 'analytic', 'stock_location_analytic'],
    'data': ['view/stock_view.xml',
             'wizard/stock_fill_inventory_view.xml'],
    'test': [
             ],
    'installable': True,
    'auto_install': False,
    
}
