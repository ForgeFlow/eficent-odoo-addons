# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Update product Qty when using Analytic locations',
    'version': '7.0.1.0.0',
    'category': 'Logistics',
    'summary': 'Update product Qty when using Analytic locations',
    'description': """
    When updating the product qty referring to an analytic account the location
    must contain the same analytic account
""",
    'author': 'Eficent',
    'website': 'http://www.eficent.com',
    'data': ['wizard/stock_change_product_qty_view.xml'],
    'depends': ['analytic', 'stock', 'stock_analytic_account_location'],
    'installable': True,
    'auto_install': False,
    
}
