# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import osv, fields, orm


class PurchaseOrder(orm.Model):
    _inherit = 'purchase.order'

    def _prepare_inv_line(self, cr, uid, account_id, order_line, context=None):
        res = super(PurchaseOrder, self)._prepare_inv_line(cr, uid,
                                                           account_id,
                                                           order_line,
                                                           context=context)
        res['order_line_sequence'] = order_line.sequence

    def _prepare_order_line_move(self, cr, uid, order, order_line, picking_id,
                                 context=None):
        res = super(PurchaseOrder, self)._prepare_order_line_move(
            cr, uid, order, order_line, picking_id, context=context)
        res['order_line_sequence'] = order_line.sequence
        return res
