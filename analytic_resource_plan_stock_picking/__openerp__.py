# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Analytic Resource Planning - get resources",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["analytic_resource_plan", "analytic_location",
                "purchase_request", "project_location",
                "analytic_resource_plan_purchase_request"],
    "description": """
Analytic Resource Planning - get resources
==============================================
Module features:
    - prepare the stock for the project
    - create Purchase request if there are not enough qty in stock

    """,
    "data": [
        "views/stock_picking_view.xml",
        "views/analytic_resource_plan_view.xml",
    ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
    'certificate': '',
}