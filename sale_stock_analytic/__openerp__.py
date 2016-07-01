# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale Stock Analytic',
    'version': '1.0',
    'category': 'Hidden',
    'summary': 'Copies the analytic account of the sales order to the stock move.',
    'description': """
Copies the analytic account of the sales order to the stock move.
""",
    'author': 'Eficent',
    'website': 'http://www.eficent.com',
    'images': ['images/deliveries_to_invoice.jpeg'],
    'depends': ['sale_stock', 'stock_move_line'],
    'init_xml': [],
    'update_xml': [
                   ],
   'data': [],
   'demo_xml': [],
    'test': [
             ],
    'installable': True,
    'auto_install': True,
    
}
