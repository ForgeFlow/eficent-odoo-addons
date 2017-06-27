# -*- coding: utf8 -*-
#
# Copyright (C) 2014 NDP Systèmes (<http://www.ndp-systemes.fr>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

{
    'name': 'Last Bin Putaway Strategy',
    'version': '0.1',
    'author': 'NDP Systèmes',
    'maintainer': 'NDP Systèmes',
    'category': '',
    'depends': ['stock'],
    'description': """
Last Bin Putaway Strategy
=========================
In a location tree where a stock is a parent location with children locations being the bins, this module implements a
new putaway strategy which sets the bin to the last bin where the product has been put in this stock.

This strategy need only to be defined once and can be applied to several locations.
""",
    'website': 'http://www.ndp-systemes.fr',
    'data': [],
    'demo': [
        'product_putaway_last_demo.xml'
    ],
    'test': [],
    'installable': False,
    'auto_install': False,
    'license': 'AGPL-3',
    'application': False,
}
