# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, osv, orm
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrder(orm.Model):
    _inherit = 'purchase.order'

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
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = super(PurchaseOrder, self).write(cr, uid, ids, line_values,
                                               context=context)
        self._reset_sequence(cr, uid, ids, context=context)
        return res


class PurchaseOrderLine(orm.Model):
    _inherit = 'purchase.order.line'

    _columns = {
        'sequence': fields.integer('Sequence',
                                   help="Gives the sequence "
                                        "order when displaying a list of "
                                        "purchase order lines.")
    }

    _defaults = {
        'sequence': 9999,
    }

    def create(self, cr, uid, values, context=None):
        if context is None:
            context = {}
        line_id = super(PurchaseOrderLine, self).create(cr, uid, values,
                                                        context=context)
        if 'order_id' in values and values['order_id']:
            self.pool['purchase.order']._reset_sequence(cr, uid,
                                                        [values['order_id']],
                                                        context=context)
        return line_id
