# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, osv, orm


class stock_picking(orm.Model):
    _inherit = 'stock.picking'

    def has_valuation_moves(self, cr, uid, move):
        """Force to return False to allow avoiding the error message,
        unless there's no linked stock moves, but moves with the name of
        the picking."""
        am_ids = self.pool.get('account.move').search(cr, uid, [
            ('ref', '=', move.picking_id.name),
        ])
        aml_obj = self.pool['account.move.line']
        aml_ids = aml_obj.search(cr, uid, [('sm_id', '!=', False)],
                                 limit=1)
        if not aml_ids and am_ids:
            return am_ids
        else:
            return False
