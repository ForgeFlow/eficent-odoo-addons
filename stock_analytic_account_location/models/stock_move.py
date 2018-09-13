# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm
from openerp.tools.translate import _


class StockMove(orm.Model):

    _inherit = "stock.move"

    def create(self, cr, uid, vals, context=None):
        src_loc = self.pool.get('stock.location').browse(
            cr, uid, vals['location_id'])
        dest_loc = self.pool.get('stock.location').browse(
            cr, uid, vals['location_dest_id'])
        add_analytic_id = False
        # if both has AA error will raise so no need to check here
        if src_loc.analytic_account_id and src_loc.usage == 'internal':
            add_analytic_id = src_loc.analytic_account_id.id
        if dest_loc.analytic_account_id and dest_loc.usage == 'internal':
            add_analytic_id = dest_loc.analytic_account_id.id
        if add_analytic_id:
            vals['analytic_account_id'] = add_analytic_id
        return super(StockMove, self).create(
            cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        check_analytic = False
        for move in self.pool.get('stock.move').browse(cr, uid, ids, context):
            if 'location_id' in vals:
                src_loc = self.pool.get('stock.location').browse(cr, uid, [vals['location_id']])[0]
                check_analytic = True
            else:
                src_loc = move.location_id

            if 'location_dest_id' in vals:
                dest_loc = self.pool.get('stock.location').browse(
                    cr, uid, [vals['location_dest_id']])[0]
                check_analytic = True
            else:
                dest_loc = move.location_dest_id

            if check_analytic:
                add_analytic_id = False
                # if both has AA error will raise so no need to check here
                if src_loc.analytic_account_id and src_loc.usage == 'internal':
                    add_analytic_id = src_loc.analytic_account_id.id
                if dest_loc.analytic_account_id and dest_loc.usage == 'internal':
                    add_analytic_id = dest_loc.analytic_account_id.id
                if add_analytic_id:
                    vals['analytic_account_id'] = add_analytic_id
        return super(StockMove, self).write(
            cr, uid, ids, vals, context=context)

    def action_done(self, cr, uid, ids, context=None):
        """Override the action_done to add constraint to check if the
        location_dest is disable"""

        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        move = self.browse(cr, uid, ids, context)[0]
        location_dest_id = move.location_dest_id
        dest_anal = move.location_dest_id.analytic_account_id
        location_id = move.location_id
        analytic = move.analytic_account_id
        if location_id.analytic_account_id and location_dest_id.analytic_account_id:
            if location_id.analytic_account_id.id != location_dest_id.analytic_account_id.id:
                raise orm.except_orm(
                    _('Validation Error'),
                    _('Cannot move between projects location, please move first to general stock.')
                )
        return super(StockMove, self).action_done(
            cr, uid, ids, context=context)
