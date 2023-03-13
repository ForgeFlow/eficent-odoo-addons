# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


{
    "name": "Project Stock Move Link",
    "version": "10.0.1.0.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": [
        "project",
        "stock_analytic_account"
    ],
    "Summary": """list the Stock Moves associated to the selected project""",
    "data": [
        "view/project_view.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True,

}
