# Copyright 2017 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Analytic Resource Planning",
    "version": "14.0.1.0.0",
    "author": "ForgeFlow, Odoo Community Association (OCA) , "
    "Matmoz, "
    "Luxim, "
    "Project Expert Team",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "category": "Project Management",
    "license": "AGPL-3",
    "depends": ["account", "purchase", "analytic_plan"],
    "data": [
        "security/ir.model.access.csv",
        "view/account_analytic_plan_version_view.xml",
        "view/account_analytic_line_plan_view.xml",
        "view/analytic_resource_plan_view.xml",
        "view/analytic_account_view.xml",
        "view/project_view.xml",
        "view/resource_plan_default.xml",
        "wizard/analytic_resource_plan_copy_version_view.xml",
        "wizard/resource_plan_line_change_state_view.xml",
    ],
    "installable": True,
}
