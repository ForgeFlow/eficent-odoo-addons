# -*- coding: utf-8 -*-
# © 2015 Akretion, Benoît GUILLOT
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Account Invoice Currency Rate',
    "summary": "Allows to handle an invoice-specific currency rate",
    'version': '8.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'author': 'Akretion, Eficent Business and IT Consulting Services S.L.',
    'website': 'http://www.akretion.com/,',
    'depends': ['account'],
    'data': [
        'wizards/force_currency_rate_view.xml',
        'views/invoice_view.xml',
    ],
    'demo': [],
    'installable': True,
}
