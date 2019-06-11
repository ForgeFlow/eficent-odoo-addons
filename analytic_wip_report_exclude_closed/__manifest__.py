# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Work In Progress Statement Exclude Closed Projects",
    "version": "10.0.2.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.,"
              "Odoo Community Association (OCA)",
    "summary": """Filter closed projects in analytic wip report""",
    "category": "Generic Modules/Projects & Services",
    "license": "AGPL-3",
    "depends": [
        "analytic_wip_report",
        "project_wbs_stage",
        "analytic_schedule",
        "analytic_wip_report_fiscalyear",
    ],
    "data": [
        "wizards/analytic_wip_report_view.xml"
    ],
    "installable": True,
}
