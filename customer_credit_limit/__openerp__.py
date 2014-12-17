# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Sistemas Adhoc
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
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
    'name': 'Customer Credit Limit',
    'version': '2.0',
    'description': """Customer Credit Limit

    A user can manually initiate the credit limit check when the quote is
    in status draft or sent.

    When approving a Sale Order it computes the sum of:
        * - The Accounts Receivable Journal Items pending to be paid
        * + The Accounts Payable Journal Items pending to be paid
        * - The total amount for Sale Orders lines approved,
        but not yet invoiced
        * - The total amount for Customer Invoices or Supplier Refunds
        that are in draft state
        * + The total amount for Supplier Invoices or Customer Refunds
        that are in draft state

    and compares it with the credit limit of the partner. If the
    credit limit is less it does not allow to approve the Sale
    Order.

    Users belonging to the group 'Sales Order Credit Block Releaser'
    will have the permission to override this rule.


    """,
    'author': 'Sistemas ADHOC, ECOSOFT, Eficent',
    'website': 'http://www.sistemasadhoc.com.ar/,http://www.ecosoft.co.th, http://www.eficent.com',
    'depends': ['account', 'sale'],
    'init_xml': [],
    'update_xml': [
        'security/check_credit_limit_security.xml',
        'security/ir.model.access.csv',
        'view/sale_workflow.xml',
        'view/sale_view.xml',
        'view/partner_view.xml',
    ],
    'demo_xml': [],
    'test': [],
    'installable': True,
}