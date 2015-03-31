# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent (<http://www.eficent.com/>)
#               <contact@eficent.com>
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

from openerp.osv import fields, orm


class stock_picking(orm.Model):
    _inherit = 'stock.picking'

    def _get_ordering_partner(self, cr, uid, picking, context=None):
        """ Gets the partner from the preceding sales order
            @param picking: object of the picking for which we are selecting
            the partner from
            @return: id of the partner
        """
        if picking.sale_id:
            return picking.sale_id.partner_id

        return super(stock_picking, self)._get_ordering_partner(
            cr, uid, picking, context=None)
