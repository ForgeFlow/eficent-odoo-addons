# Copyright 2015 Odoo SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Analytic Journal",
    "version": "14.0.1.0.0",
    "summary": "Analytic Journals as in previous Odoo versions",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "author": "ForgeFlow",
    "license": "LGPL-3",
    "category": "Analytic",
    "depends": ["account", "analytic"],
    "data": [
        "views/analytic_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
