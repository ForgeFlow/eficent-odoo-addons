# Copyright 2015-17 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": "Products Manufacturer Partner",
    "version": "14.0.1.0.0",
    "author": "ForgeFlow",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "license": "AGPL-3",
    "category": "Purchase Management",
    "summary": """
    Classify manufacturers by providing an indicator in the partner.
    In the product, select a manufacturer from the list of partners where
    this indicator has been set.
     """,
    "depends": ["purchase", "product_manufacturer"],
    "data": [
        "view/partner_view.xml",
        "view/product_view.xml",
    ],
    "installable": True,
}
