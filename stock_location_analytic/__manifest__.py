# Copyright 2017-23 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Location Analytic",
    "version": "15.0.1.0.0",
    "category": "Logistics",
    "summary": "Introduces the analytic account to the locations",
    "author": "ForgeFlow",
    "license": "AGPL-3",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "depends": ["stock", "analytic", "analytic_location"],
    "data": [
        "views/stock_view.xml",
        "views/analytic_view.xml",
    ],
    "demo": ["demo/stock_demo.xml"],
    "installable": True,
}
