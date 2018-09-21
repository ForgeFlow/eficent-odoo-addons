# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lpgl.html).


{
    'name': 'Account Move Check Number',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': "Eficent, "
              "Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/bank-payment',
    'category': 'Banking addons',
    'depends': [
        'account',
    ],
    'data': [
        'views/account_move_view.xml',
    ],
    'installable': True,
}
