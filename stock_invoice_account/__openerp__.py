# -*- coding: utf-8 -*-
##############################################################################
#
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
    'name': 'Stock invoice account',
    'version': '1.0',
    'author': 'Eficent',
    'website': 'http://www.eficent.com',
    'description': """
Stock Invoice Account
======================
This module determines the supplier's invoice account as the product's
stock input account, when the invoice is created from the
stock move, only when the associated stock move is either
outbound from one of the company warehouses (returns), or inbound to the
company.

""",
    'images': [],
    'depends': ['stock', 'stock_picking_invoice_link'],
    'category': 'Warehouse Management',
    'demo': [],
    'data': [],
    'auto_install': False,
    'installable': True,
}
