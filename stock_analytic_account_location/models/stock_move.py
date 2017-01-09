# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm


class StockMove(orm.Model):

    _inherit = "stock.move"

    def create(self, cr, uid, vals, context=None):
        src_loc = self.pool.get('stock.location').browse(
            cr, uid, vals['location_id'])
        dest_loc = self.pool.get('stock.location').browse(
            cr, uid, vals['location_dest_id'])
        add_analytic_id = False
        if src_loc.analytic_account_id and dest_loc.analytic_account_id:
            if (src_loc.usage == 'customer'and dest_loc.usage ==
                'internal') or (src_loc.usage == 'internal' and
                   dest_loc.usage == 'customer'):
                add_analytic_id = dest_loc.analytic_account_id.id
        if src_loc.analytic_account_id and not dest_loc.analytic_account_id:
            if ((src_loc.usage == 'internal' and
                dest_loc.usage != 'internal')) or (
                (src_loc.usage == 'customer' and
                 dest_loc.usage == 'internal')):
                add_analytic_id = src_loc.analytic_account_id.id
        if not src_loc.analytic_account_id and dest_loc.analytic_account_id:
            if src_loc.usage == 'supplier':
                add_analytic_id = dest_loc.analytic_account_id.id
            if src_loc.usage in ('inventory', 'customer') and \
                 dest_loc.usage == 'internal':
                add_analytic_id = dest_loc.analytic_account_id.id
        if add_analytic_id:
            vals['analytic_account_id'] = add_analytic_id
        return super(StockMove, self).create(
            cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        moves = self.browse(cr, uid, ids, context=context)
        add_analytic_id = 0
        for move in moves:
            src_loc = move.location_id
            dest_loc = move.location_dest_id
            if src_loc.analytic_account_id and dest_loc.analytic_account_id:
                if (src_loc.usage == 'customer'and dest_loc.usage ==
                    'internal') or (src_loc.usage == 'internal' and
                       dest_loc.usage == 'customer'):
                    add_analytic_id = dest_loc.analytic_account_id.id
            if src_loc.analytic_account_id and not dest_loc.analytic_account_id:
                if (src_loc.usage == 'internal' and
                    dest_loc.usage != 'internal') or \
                    (src_loc.usage == 'customer' and
                     dest_loc.usage == 'internal'):
                    add_analytic_id = src_loc.analytic_account_id.id
            if not src_loc.analytic_account_id and dest_loc.analytic_account_id:
                if (src_loc.usage in ('internal', 'supplier') and \
                                dest_loc.usage != 'internal') or \
                    (src_loc.usage == 'customer' and
                     dest_loc.usage == 'internal'):
                    add_analytic_id = dest_loc.analytic_account_id.id
            if add_analytic_id:
                vals['analytic_account_id'] = add_analytic_id
        return super(StockMove, self).write(
            cr, uid, ids, vals, context=context)

    def _check_analytic_account(self, cr, uid, ids, context=None):
        for move in self.browse(cr, uid, ids):
            if move.location_id and move.location_dest_id:
                if move.location_id.analytic_account_id and move.location_dest_id.analytic_account_id:
                    if move.location_id.analytic_account_id.id != move.location_dest_id.analytic_account_id.id:
                        return False
        return True

    _constraints = [(_check_analytic_account,
                     "Cannot move between different projects locations, "
                     "please move first to general stock",
                     ['location_io', 'location_dest_id'])]
