# -*- coding: utf-8 -*-
# © 2015 Akretion, Benoît GUILLOT
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase Currency Rate',
    "summary": "Allows to handle an purchase-specific currency rate",
    'version': '8.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'author': 'Eficent',
    'website': 'http://www.eficent.com/,',
    'depends': ['purchase',
                'account_invoice_currency_rate'
    ],
    'data': [
        'wizards/purchase_force_currency_rate_view.xml',
        'wizards/picking_force_currency_rate_view.xml',
        'views/purchase_view.xml',
        'views/stock_view.xml'
    ],
    'demo': [],
    'installable': True,
}
