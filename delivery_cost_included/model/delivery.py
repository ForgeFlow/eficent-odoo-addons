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

from openerp.osv import fields,osv


class delivery_carrier(osv.osv):
    _inherit = "delivery.carrier"

    _columns = {
        'partner_id': fields.many2one('res.partner', 'Transport Company',
                                      required=False,
                                      help="The partner that is doing the delivery"
                                           " service."),
        'product_id': fields.many2one('product.product',
                                      'Delivery Product',
                                      required=False),
        'cost_included': fields.boolean(
            'Cost included',
            help="If this field is set, no product will be added "
                 "to the sale order or invoice. It is assumed that  "
                 "the sale price includes the delivery costs."),
    }

    _defaults = {
        'cost_included': False,
    }

delivery_carrier()
