# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Stock Cancel Reverse Account Move',
    'version': '7.0.1.0.0',
    'category': 'Warehouse',
    'author':  'Eficent Business and IT Consulting Services S.L.',
    'website': 'http://www.eficent.com',
    'summary': 'Reverses the account move of a stock move the later is '
               'cancelled',
    'depends': [
        'stock_cancel',
        'stock_move_entries',
    ],
    'data': [],
    'demo': [],
    'test': [],
    'application': False,
}
