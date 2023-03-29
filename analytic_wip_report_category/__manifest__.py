# Copyright 2023 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Work In Progress Statement Analytic Categories",
    "version": "15.0.1.0.0",
    "author": "ForgeFlow,Odoo Community Association (OCA)",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "summary": """Filter categories in analytic wip report""",
    "category": "Generic Modules/Projects & Services",
    "license": "AGPL-3",
    "depends": [
        "analytic_wip_report_extend",
        "analytic_category",
        "analytic_wip_report_exclude_closed",
    ],
    "data": ["wizards/analytic_wip_report_view.xml"],
    "installable": True,
}
