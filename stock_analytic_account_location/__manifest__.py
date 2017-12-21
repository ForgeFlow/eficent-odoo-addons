# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Stock Analytic Account Location',
    'version': '10.0.1.0.0',
    'category': 'Logistics',
    'summary': 'Stock analytic account using analytic locations',
    'author': 'Eficent, Odoo Community Association (OCA)',
    'website': 'http://www.eficent.com',
    "license": "AGPL-3",
    'depends': [
        'stock',
        'analytic',
        'account_analytic_parent',
        'stock_location_analytic'
    ],
    'installable': True,
}
