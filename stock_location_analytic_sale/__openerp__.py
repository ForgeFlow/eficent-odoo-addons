# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale Location Analytic',
    'version': '7.0.1.0.0',
    'category': 'Logistics',
    'summary': 'Sales using analytic locations',
    'description': """
    For sales, the source location should contain the same analytic account
    than the order. If it's a dropship two movements have to be done at the
    same time
""",
    'author': 'Eficent',
    'website': 'http://www.eficent.com',
    'depends': ['stock_analytic_account_location', 'sale',
                'sale_stock_analytic'],
    'data': ['views/sale_view.xml'],
    'installable': True,
    'auto_install': False,
    
}
