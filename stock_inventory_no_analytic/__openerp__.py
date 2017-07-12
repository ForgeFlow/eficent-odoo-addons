# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Inventory No Analytic",
    "version": "7.0.1.0.0",
    "author": "Eficent",
    "license": 'AGPL-3',
    "website": "www.eficent.com",
    'summary': 'Create an inventory of stock non related to projects',
    "depends": ["stock", "stock_analytic_account"],
    'data': ['wizard/stock_fill_inventory_view.xml',
    ],
    'installable': True,
}
