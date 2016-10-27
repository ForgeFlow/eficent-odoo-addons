# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Analytic Reserve",
    "summary": "Introduces the option to reserve / unreserve stock for a "
               "specific analytic account / project.",
    "version": "8.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "Warehouse",
    "depends": ["stock", "analytic", "stock_analytic_account"],
    "license": "AGPL-3",
    "data": [
        "security/stock_analytic_reserve_security.xml",
        "security/ir.model.access.csv",
        "data/stock_analytic_reserve_data.xml",
        "data/stock_analytic_reserve_sequence.xml",
        "views/stock_analytic_reserve_view.xml",
        "views/stock_warehouse_view.xml",
    ],
    'installable': True,
}
