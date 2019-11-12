# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Move Category",
    "version": "12.0.1.0.0",
    "author": "Eficent, Odoo Community Association (OCA)",
    "website": "http://www.eficent.com",
    "category": "Generic",
    "depends": ["account", "analytic"],
    "summary": "Adds a category field in the account move line",
    "license": "AGPL-3",
    "data": [
        "views/account_move_view.xml",
    ],
    'installable': True,
}
