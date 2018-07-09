# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Analytic Cost and Revenue",
    "version": "10.0.1.0.0",
    "author": "Eficent",
    "category": "Projects",
    "Summary": "Analytic Cost and Revenue to analytic accounts ",
    "website": "http://www.eficent.com/",
    "license": "AGPL-3",
    "depends": [
        "account",
        "analytic",
        "account_analytic_parent",
        "analytic_journal",
    ],
    "data": [
        "views/analytic_view.xml"
    ],
    "installable": True,
}
