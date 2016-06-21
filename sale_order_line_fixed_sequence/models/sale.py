# -*- coding: utf-8 -*-
#
#    Jamotion GmbH, Your Odoo implementation partner
#    Copyright (C) 2013-2015 Jamotion GmbH.
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
#    Created by Boris on 15.03.16.
#
from openerp.osv import fields, osv, orm
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(orm.Model):
    _inherit = 'sale.order'

    def _reset_sequence(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for rec in self.browse(cr, uid, ids, context=context):
            current_sequence = 1
            for line in rec.order_line:
                line.write({'sequence': current_sequence})
                current_sequence += 1

    # reset line sequence number during write
    def write(self, cr, uid, ids, line_values, context=None):
        if context is None:
            context = {}
        res = super(SaleOrder, self).write(cr, uid, ids, line_values,
                                           context=context)
        self._reset_sequence(cr, uid, ids, context=context)
        return res


class SaleOrderLine(orm.Model):
    _inherit = 'sale.order.line'

    _columns = {
        'sequence': fields.integer('Sequence',
                                   help="Gives the sequence "
                                        "order when displaying a list of "
                                        "sales order lines.", default=99999)
    }

    def create(self, cr, uid, values, context=None):
        if context is None:
            context = {}
        line_id = super(SaleOrderLine, self).create(cr, uid, values,
                                                    context=context)
        if 'order_id' in values and values['order_id']:
            self.pool['sale.order']._reset_sequence(cr, uid,
                                                    [values['order_id']],
                                                    context=context)
        return line_id
