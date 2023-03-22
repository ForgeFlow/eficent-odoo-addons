# Copyright 2023 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Analytic Category",
    "summary": """Allow to define analytic categories for analytic accounts""",
    "version": "15.0.1.0.0",
    "author": "ForgeFlow",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "category": "Analytic",
    "license": "LGPL-3",
    "depends": ["analytic"],
    "data": [
        "security/security.xml",
        "view/analytic_view.xml",
        "view/category_view.xml",
    ],
    "installable": True,
}
