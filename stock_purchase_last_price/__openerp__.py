# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

{
    "name": "Stock Move Last Purchase Price Info",
    "version": "7.0.1.0.0",
    "category": "Purchase Management",
    "license": "AGPL-3",
    "author": "Eficent, "
              "Odoo Community Association (OCA)",
    "website": "http://www.eficent.io",
    "depends": [
        "stock",
        "purchase",
    ],
    "data": [
        "views/stock_view.xml",
    ],
    "installable": True,
}
