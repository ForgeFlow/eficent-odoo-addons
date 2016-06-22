# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, osv, orm
import logging

_logger = logging.getLogger(__name__)


class StockPicking(orm.Model):
    _inherit = 'stock.picking'

    def _reset_sequence(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for rec in self.browse(cr, uid, ids, context=context):
            current_sequence = 1
            for line in rec.move_lines:
                line.write({'sequence': current_sequence})
                current_sequence += 1

    # reset line sequence number during write
    def write(self, cr, uid, ids, line_values, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = super(StockPicking, self).write(cr, uid, ids, line_values,
                                              context=context)
        self._reset_sequence(cr, uid, ids, context=context)
        return res


class StockMove(orm.Model):
    _inherit = 'stock.move'

    _columns = {
        'sequence': fields.integer('Sequence',
                                   help="Gives the sequence "
                                        "order when displaying a list of "
                                        "stock moves for a picking.",
                                   default=99999)
    }

    def create(self, cr, uid, values, context=None):
        if context is None:
            context = {}
        line_id = super(StockMove, self).create(cr, uid, values,
                                                context=context)
        if 'picking_id' in values and values['picking_id']:
            self.pool['stock.picking']._reset_sequence(cr, uid,
                                                       [values['picking_id']],
                                                       context=context)
        return line_id
