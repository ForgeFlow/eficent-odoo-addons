# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Purchase Last Price Info",
    "version": "10.0.1.0.0",
    "category": "Purchase Management",
    "license": "AGPL-3",
    "author": "Eficent, "
              "Odoo Community Association (OCA)",
    "website": "http://www.eficent.com",
    "depends": [
        "sale",
        "sale_order_dates",
        "purchase",
    ],
    "data": [
        "views/sale_view.xml",
    ],
    "installable": True,
}
