# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Analytic Contract Value",
    "version": "7.0.1.0.0",
    "summary": "Sets a Contract Value on the analytic account",
    "author": "Eficent",
    "website": "http://www.eficent.com",
    "category": "Generic",
    "depends": ["analytic"],
    "license": "AGPL-3",
    "data": [
        "security/analytic_security.xml",
        "wizards/analytic_change_contract_value_view.xml",
        "wizards/accounts_with_contract_value_view.xml",
        "views/analytic_account_view.xml",

    ],
    'installable': True,
    'active': False,
}
