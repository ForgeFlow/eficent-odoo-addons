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
        """ Gets the partner from the preceding order
            Note that this function should inherited in related sale and
            purchase
            modules
            @param picking: object of the picking for which we are selecting
            the partner from
            @return: object of the partner
        """
        return picking.partner_id

    def _get_partner_invoice_id(self, cr, uid, ids, field_name, arg,
                                context=None):
        res = {}
        for picking in self.browse(cr, uid, ids, context=context):
            partner  = self._get_partner_to_invoice(cr, uid, picking,
                                                    context=context)
            if isinstance(partner, int):
                res[picking.id] = partner
            else:
                res[picking.id] = partner.id or False
        return res

    def _get_partner_order_id(self, cr, uid, ids, field_name, arg,
                              context=None):
        res = {}
        for picking in self.browse(cr, uid, ids, context=context):
            partner = self._get_ordering_partner(cr, uid, picking,
                                                context=context)
            if isinstance(partner, int):
                res[picking.id] = partner
            else:
                res[picking.id] = partner.id or False
        return res

    _columns = {
        'partner_invoice_id': fields.function(_get_partner_invoice_id,
                                              method=True,
                                              string='Invoice Address',
                                              type='many2one',
                                              relation="res.partner",
                                              readonly=True,
                                              store=False),
        'partner_order_id': fields.function(_get_partner_order_id,
                                            method=True,
                                            string='Delivery Address',
                                            type='many2one',
                                            relation="res.partner",
                                            readonly=True,
                                            store=False)
    }


class stock_picking_in(orm.Model):

    _inherit = "stock.picking.in"

    def __init__(self, pool, cr):
        super(stock_picking_in, self).__init__(pool, cr)
        self._columns['partner_invoice_id'] = \
            self.pool['stock.picking']._columns['partner_invoice_id']
        self._columns['partner_order_id'] = \
            self.pool['stock.picking']._columns['partner_order_id']


class stock_picking_out(orm.Model):

    _inherit = "stock.picking.out"

    def __init__(self, pool, cr):
        super(stock_picking_out, self).__init__(pool, cr)
        self._columns['partner_invoice_id'] = \
            self.pool['stock.picking']._columns['partner_invoice_id']
        self._columns['partner_order_id'] = \
            self.pool['stock.picking']._columns['partner_order_id']
