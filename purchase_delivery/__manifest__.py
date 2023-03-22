# Copyright 2015-17 ForgeFlow S.L. <contact@forgeflow.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Delivery Costs",
    "version": "15.0.1.0.0",
    "category": "Purchase Management",
    "summary": """Allows you to add delivery methods in purchase orders
    and pickings""",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "license": "AGPL-3",
    "depends": ["delivery", "purchase_analytic"],
    "data": [
        "view/purchase_view.xml",
        "view/delivery_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
