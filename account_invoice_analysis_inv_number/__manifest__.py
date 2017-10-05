# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Invoices Analysis by invoice number",
    "version": "10.0.1.0.0",
    "Summary": """This module is meant to extend the report 'Invoices Analysis'
        adding the invoice internal number, the supplier invoice number and
        the journal entry.This is useful to allow the user to drill down.""",
    "category": "Accounting & Finance",
    "author": "Eficent,"
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "account",
    ],
    "data": [
        "report/account_invoice_report_view.xml",
    ],
    "installable": True,
}
