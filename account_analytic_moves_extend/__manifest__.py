# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Analytic moves only for expenses and revenues",
    "version": "10.0.1.0.0",
    "author": "Eficent, Odoo Community Association (OCA)",
    "license": 'AGPL-3',
    "website": "www.eficent.com",
    "summary": """Limits the creation of analytic lines associated to
        invoices accepted only when the move is associated to an expense or
        revenue account.
    """,
    "depends": [
        "account",
        "analytic"
    ],
    "installable": True,
}
