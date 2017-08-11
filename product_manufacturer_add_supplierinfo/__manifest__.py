# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product manufacturer add supplier info",
    "summary": """ The manufacturer indicated in the product is automatically
               added as a vendor in the supplier info.""",
    "version": "10.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L,"
              "Serpent Consulting Services Pvt. Ltd.,",
    "website": "www.eficent.com",
    "category": "Purchase Management",
    "depends": [
        "product",
        "product_manufacturer"
    ],
    'installable': True,
}
