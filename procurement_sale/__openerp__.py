# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Procurement Sale",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Purchase Management",
    "depends": ["sale_stock"],
    "description": """
Procurement Sale
================
This module introduces sales order line into the procurement order.

Credits
=======

Contributors
------------

* Jordi Ballester <jordi.ballester@eficent.com>

    """,
    "data": [
        "views/procurement_view.xml",
    ],
    'installable': True,
    'active': False,
}
