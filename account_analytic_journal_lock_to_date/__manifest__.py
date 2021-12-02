# -*- coding: utf-8 -*-
# Copyright 2021 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Journal Lock Date',
    'summary': """
        Lock each journal independently""",
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'ForgeFlow S.L.,Odoo Community Association (OCA)',
    'website': 'https://acsone.eu/',
    'depends': [
        'analytic_journal',
        'account_analytic_parent'
    ],
    'data': [
        'views/account_analytic_journal.xml',
        'views/analytic_account_view.xml',
    ],
}
