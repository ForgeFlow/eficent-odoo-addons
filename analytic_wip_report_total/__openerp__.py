# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

{
    "name": "Totals in analytic wip report view",
    "version": "1.0", 
    "author": "Eficent",
    "category": "Projects",
    "description": """
Sale for PRI
============
Contains customizations for PRI
- In the order lines to invoice view add the product

""", 
    "website": "http://www.eficent.com/",
    "license": "", 
    "depends": [
        "analytic_wip_report_fiscalyear",
        "analytic_wip_report_contract_value",
    ],
    "demo": [],
    "data": [
        'views/wip_report_view.xml',
    ], 
    "test": [], 
    "js": [], 
    "css": [], 
    "qweb": [], 
    "installable": True, 
    "auto_install": False, 
    "active": False
}