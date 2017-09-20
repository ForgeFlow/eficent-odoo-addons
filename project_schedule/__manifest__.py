# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Project Schedule",
    "version": "10.0.1.0.0",
    "summary": """Automatically computes start and end dates for
               projects based on the earliest start and latest finish date
               of the children.""",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": [
        "analytic",
        "account_analytic_parent"
    ],
    'installable': True,
}
