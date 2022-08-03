# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#  - Jordi Ballester Alomar
# Copyright 2017 MATMOZ d.o.o.
#  - Matjaž Mozetič
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Stock Analytic",
    "version": "10.0.2.0.0",
    "author": "Eficent, Odoo Community Association (OCA),"
              "Project Expert Team",
    "website": "http://project.expert",
    "category": "Project Management",
    "license": "AGPL-3",
    "depends": [
        "purchase",
        "stock_analytic_account",
        "purchase_analytic",
        "purchase_location_by_line",
        "account_analytic_parent"
    ],
    'data': [
        'views/purchase_views.xml',
    ],
    "installable": True,
}
