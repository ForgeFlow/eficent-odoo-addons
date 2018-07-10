# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Location in Project",
    "version": "10.0.1.0.0",
    "author": "Eficent, Odoo Community Association (OCA)",
    "license": 'AGPL-3',
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "summary": """stock location in the project.""",
    "depends": [
        "project_stock",
        "analytic_location"
    ],
    "data": [
        "view/project_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
