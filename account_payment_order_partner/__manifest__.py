# -*- coding: utf-8 -*-
# © 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Account Payment Order Partner',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': "Eficent, "
              "Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/bank-payment',
    'category': 'Banking addons',
    'depends': [
        'account_payment_order',
    ],
    'data': [
        'wizard/account_payment_line_create_view.xml',
    ],
    'installable': True,
}
