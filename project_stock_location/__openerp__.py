# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


{
    "name": "Project Stock Location No Reserve",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["project_stock", "stock_analytic_account"],
    "description": """
Not reserve stock for projects anymore

    """,
    "init_xml": [],
    "data": [
        "view/project_view.xml",
        "view/account_analytic_account_view.xml",
    ],
    'installable': True,
    'active': False,
    'certificate': '',
    'application': False,
}
