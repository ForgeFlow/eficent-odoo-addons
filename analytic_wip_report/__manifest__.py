# Copyright 2015 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Work In Progress Statement",
    "version": "15.0.1.0.0",
    "author": "ForgeFlow, Odoo Community Association (OCA), " "Project Expert Team",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "category": "Project Management",
    "license": "AGPL-3",
    "depends": [
        "analytic",
        "analytic_plan_cost_revenue",
        "project_wbs",
        "project_wbs_stage",
        "analytic_journal",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_analytic_account_view.xml",
        "wizards/analytic_wip_report_view.xml",
    ],
    "installable": True,
}
