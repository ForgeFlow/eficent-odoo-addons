# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase Stock Location Analytic',
    'version': '7.0.1.0.0',
    'category': 'Logistics',
    'summary': 'Purchases using analytic locations',
    'description': """
    When buying and the analytic account is set in the line, the destination
    location should contain that analytic account
""",
    'author': 'Eficent',
    'website': 'http://www.eficent.com',
    'depends': ['stock_analytic_account_location', 'purchase',
                'purchase_stock_analytic'],
    'installable': True,
    'auto_install': False,
    
}
