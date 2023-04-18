# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Analytic Resource Plan MRP",
    "version": "10.0.1.0.0",
    "description": """Analytic Resource Plan MRP""",
    "author": "Eficent",
    "website": "www.eficent.com",
    "license": "AGPL-3",
    "category": "Generic Modules/Projects & Services",
    "depends": [
        "analytic_resource_plan",
        "mrp",
        "analytic_location",
    ],
    "data": [
        "wizard/consume_view.xml",
        "wizard/produce_view.xml",
        "views/analytic_resource_plan_line_view.xml",
    ],
    'installable': True,
}
