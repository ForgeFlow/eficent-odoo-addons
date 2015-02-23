# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#             <contact@eficent.com>
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
    'name': 'Products Manufacturer Partner',
    'version': '1.0',
    'author': 'Eficent',
    "website": "www.eficent.com",
    'category': 'Purchase Management',
    'depends': ['product_manufacturer'],
    'demo': [],
    'description': """
A module that classifies partners as manufacturers
==================================================
This module helps to better classify manufacturers by providing an indicator
in the partner.

In the product, a user can only select a manufacturer from the list of partners
where this indicator has been set.

    """,
    'data': [
        'view/partner_view.xml',
    ],
    'auto_install': False,
    'installable': True,
    'images': [],
}
