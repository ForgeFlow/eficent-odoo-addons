# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

{
    "name": "Totals in analytic wip report view",
    "version": "9.0.1.0.0",
    "author": "Eficent",
    "category": "Projects",
    "summary": """
        Add the totals in tree view

""", 
    "website": "http://www.eficent.com/",
    "license": "LGPL-3",
    "depends": [
        "analytic_wip_report_extend",
    ],
    "data": [
        'views/wip_report_view.xml',
    ],
    "installable": True,
}
