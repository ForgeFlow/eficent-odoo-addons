# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


{
    "name": "Work In Progress Statement Exclude Closed Projects",
    "version": "1.0",
    "author": "Eficent",
    "website": "",
    "category": "Generic Modules/Projects & Services",
    "depends": [
                "analytic_wip_report",
                "analytic_wip_report_fiscalyear",
                ],
    "description": """
Work In Progress Statement
====================================
Filter closed projects in analytic wip report

More information and assistance:
-----------------------------------
    If you are interested in this module and seek further assistance to use it please visit
    us at www.eficent.com or conact us at contact@eficent.com.

    """,

    'data': [
        "wizards/analytic_wip_report_view.xml"
    ],
    'test':[
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}