# Copyright 2017-23 ForgeFlow S.L.
# Copyright 2017-19 Luxim d.o.o.
# Copyright 2017-19 Matmoz d.o.o.
# Copyright 2017-19 Deneroteam.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Project WBS Stage",
    "version": "15.0.1.0.0",
    "author": "Eficent,ForgeFlow",
    "license": "LGPL-3",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "category": "Generic Modules/Projects & Services",
    "summary": """Add the stage to the project wbs
    """,
    "depends": ["project_wbs", "analytic"],
    "data": [
        "views/account_analytic_account_view.xml",
    ],
    "installable": True,
}
