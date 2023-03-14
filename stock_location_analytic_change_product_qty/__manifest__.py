# Copyright 2023 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Update Product Qty Analytic",
    "version": "15.0.1.0.0",
    "category": "Analytic",
    "summary": "Update product Qty when using Analytic locations",
    "author": "ForgeFlow",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "license": "AGPL-3",
    "depends": ["analytic", "stock", "stock_analytic_account"],
    "data": ["wizard/stock_change_product_qty.xml"],
    "installable": True,
    "auto_install": False,
}
