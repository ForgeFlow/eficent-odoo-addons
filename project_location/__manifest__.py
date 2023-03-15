# © 2023 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Location in Project",
    "version": "15.0.1.0.0",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "category": "Generic Modules/Projects & Services",
    "summary": """stock location in the project.""",
    "depends": ["project_wbs", "analytic_location"],
    "data": [
        "view/project_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
