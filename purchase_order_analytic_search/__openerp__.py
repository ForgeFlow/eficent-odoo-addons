# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Purchase Order Analytic Search",
    "version": "9.0.1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["analytic", "purchase"],
    "description": """
Search purchase orders by analytic account. New menu entry in Purchasing to
list purchase order lines.
""",
    "data": [
        "views/purchase_order_view.xml",
    ],
    'installable': True,
    'active': False,
}
