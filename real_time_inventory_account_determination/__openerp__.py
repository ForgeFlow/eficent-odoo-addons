# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Real-Time Inventory Account Determination',
    'version': '1.0',
    'author': 'Eficent',
    'website': 'http://www.eficent.com',
    'description': """

Real-Time Inventory Account Determination
=========================================
This module aims to determine the correct accounts when perpetual (real-time)
inventory is going to be used for a product.

Product / Product Category Accounts
-----------------------------------
For a product to be correctly defined under the perpetual inventory
accounting the following settings are required in the product or the product
category.

* Stock Input Account:
Should map to an Account of type 'Liability'. It is generally called 'Goods
Received Not Invoiced' (GRIN) or 'Goods Receipt /  Invoice Receipt' (GR/IR).

* Stock Output Account:
Should map to an Account of type 'Expense'. The account is generally called
'Cost of Goods Sold' (COGS).

* Stock Valuation Account:
Should map to an Account of type 'Asset'. This account is generally called
'Stock'.

* Price Difference Account:
Should map to an Account of type 'Expense' that is intended to capture the
price differences between the cost of the product indicated in the PO and
that shown in the invoice.

* Income Account:
Should map to an Account of type 'Revenue' that is intended to capture the
revenue originated from the sale of this product.

* Expense Account:
Should map to the same account as in 'Stock Output Account'.

Creating Supplier Invoices
--------------------------
When a supplier invoice is created from a Purchase Order or Picking,
irrespective of the invoice control method of the PO, the following accounts
are determined in the invoice line for products (not services) with
real-time inventory valuation.

Products moving into or returning to the supplier from one of the
company's internal locations: Stock Input Account defined in the product or
product category.

Products moving into a third party (drop shipments) or returning from a
third party: the Expense Account (because the stockable item is not going to
be subject to the company inventory valuation, but treated as an expense).

When a supplier invoice is created, not from a Purchase Order or Picking
but from scratch the application will propose by default the Expense
Account. This can be understood in the context of supplier refunds, where
the company wants to refer to the original product in the invoice, but the
product is not physically returned to the supplier (perhaps because it was
damaged and it is scrapped).

Validating Supplier Invoices
----------------------------
The GRNI (Goods Received Not Invoiced) account is credited when the product
is received into stock, at the price indicated in the PO for that product.

At the time of validating the supplier invoice, when the application
prepares the account moves, the GRNI account will be debited with the same
amount as it was credited originally, and the difference between the invoice
line subtotal and the amount of the product received will be posted to the
product or product category 'Price Difference Account'.

Other information
-----------------
This module depends on the module "stock_picking_invoice_link" maintained
in OCA repository 'stock-logistics-workflow'.
See: https://github.com/OCA/stock-logistics-workflow/tree/7.0

""",
    'images': [],
    'depends': ['product', 'purchase', 'stock_picking_invoice_link'],
    'category': 'Accounting & Finance',
    'demo': [],
    'data': ['view/product_view.xml',],
    'auto_install': False,
    'installable': True,
}
