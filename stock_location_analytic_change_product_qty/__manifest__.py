# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Update Product Qty Analytic",
    "version": "12.0.1.0.0",
    "category": "Analytic",
    "summary": "Update product Qty when using Analytic locations",
    "author": "Eficent",
    "website": "http://www.eficent.com",
    "license": "AGPL-3",
    "depends": ["analytic", "stock", "stock_analytic_account"],
    "data": ["wizard/stock_change_product_qty.xml"],
    "installable": True,
    "auto_install": False,
}
