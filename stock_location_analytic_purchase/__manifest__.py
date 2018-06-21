# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase Stock Location Analytic',
    'version': '10.0.1.0.0',
    'category': 'Analytic',
    'summary': 'Purchases using analytic locations',
    'author': 'Eficent',
    'website': 'http://www.eficent.com',
    'depends': [
        'analytic',
        'stock_analytic_account',
        'purchase',
        'purchase_stock_analytic'
    ],
    'data': [
        'views/purchase_views.xml',
    ],
    'installable': True,
}
