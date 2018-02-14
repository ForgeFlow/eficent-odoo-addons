# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


{
    "name": "Work In Progress Statement Extend",
    "version": "7.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "category": "Projects",
    "description": """
Work In Progress Statement
======================================
Add new fields to analytic wop statement report

""",
    "website": "http://www.eficent.com/",
    "license": "",
    "depends": [
        "analytic_wip_report", "account_move_category",
        "analytic_wip_report_fiscalyear",
    ],
    "data": [
        "account_analytic_account_view.xml",
    ],
    "installable": True,
    "auto_install": False,
    "active": False
}
