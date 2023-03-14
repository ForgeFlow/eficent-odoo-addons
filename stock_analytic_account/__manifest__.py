# Copyright 2023 ForgeFlow S.L.
# Copyright 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Analytic Account",
    "version": "15.0.1.0.0",
    "author": "ForgeFlow, Odoo Community Association (OCA)," "Project Expert Team",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "category": "Project Management",
    "license": "AGPL-3",
    "depends": [
        "stock_analytic",
        "stock_location_analytic",
        "analytic_location",
        "analytic_journal",
    ],
    "data": [
        "view/stock_view.xml",
        "view/stock_picking_view.xml",
        "view/analytic_account_view.xml",
    ],
    "pre_init_hook": "pre_init_hook",
    "installable": True,
}
