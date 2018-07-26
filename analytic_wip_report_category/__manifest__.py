# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Work In Progress Statement Analytic Categories",
    "version": "10.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.,"
              "Odoo Community Association (OCA)",
    "summary": """Filter categories in analytic wip report""",
    "category": "Generic Modules/Projects & Services",
    "license": "AGPL-3",
    "depends": [
        "analytic_wip_report_extend",
        "analytic_category",
    ],
    "data": [
        "wizards/analytic_wip_report_view.xml"
    ],
    "installable": True,
}
