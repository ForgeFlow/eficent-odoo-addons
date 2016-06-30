# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Move Order Sequence",
    "description": "Shows the sales/purchase order line in the pickings and "
                   "propagates it to the invoice lines.",
    "version": "7.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "category": "Warehouse",
    "website": "http://www.eficent.com/",
    "license": "AGPL-3", 
    "depends": [
        "stock",
        "account_invoice_line_order_sequence"
    ], 
    "demo": [], 
    "data": [
        "view/stock_picking_view.xml"
    ],
    "installable": True, 
    "auto_install": False, 
    "active": False
}
