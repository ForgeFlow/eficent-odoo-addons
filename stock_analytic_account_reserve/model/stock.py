# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
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
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import logging
from openerp import netsvc
_logger = logging.getLogger(__name__)
from openerp.tools import float_compare


class StockMove(orm.Model):

    _inherit = "stock.move"

    _columns = {
        'analytic_reserved': fields.boolean(
            'Reserved',
            help="Reserved for the Analytic Account"),
    }

    def _get_analytic_reserved(self, cr, uid, vals, context=None):
        context = context or {}
        analytic_obj = self.pool['account.analytic.account']
        aaid = vals['analytic_account_id']
        if aaid:
            aa = analytic_obj.browse(cr, uid, aaid, context=context)
            return aa.use_reserved_stock
        else:
            return False

    def create(self, cr, uid, vals, context=None):
        if 'analytic_account_id' in vals:
            vals['analytic_reserved'] = self._get_analytic_reserved(
                cr, uid, vals, context=context)
        return super(StockMove, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if 'analytic_account_id' in vals:
            vals['analytic_reserved'] = self._get_analytic_reserved(
                cr, uid, vals, context=context)
        return super(StockMove, self).write(cr, uid, ids, vals,
                                            context=context)

    def action_scrap(self, cr, uid, ids, quantity, location_id, context=None):
        """ Move the scrap/damaged product into scrap location
        @param cr: the database cursor
        @param uid: the user id
        @param ids: ids of stock move object to be scrapped
        @param quantity : specify scrap qty
        @param location_id : specify scrap location
        @param context: context arguments
        @return: Scraped lines
        Attention!!! This method overrides the standard without calling Super
        The changes introduced by this module are encoded within a
        comments START OF and END OF stock_analytic_account.
        """

        # quantity should in MOVE UOM
        if quantity <= 0:
            raise osv.except_osv(
                _('Warning!'),
                _('Please provide a positive quantity to scrap.'))
        res = []
        for move in self.browse(cr, uid, ids, context=context):
            source_location = move.location_id
            if move.state == 'done':
                source_location = move.location_dest_id
            if source_location.usage != 'internal':
                # restrict to scrap from a virtual location
                # because it's meaningless and it may introduce
                # errors in stock ('creating' new products from nowhere)
                raise osv.except_osv(
                    _('Error!'),
                    _('Forbidden operation: it is not allowed '
                      'to scrap products from a virtual location.'))
            move_qty = move.product_qty
            uos_qty = quantity / move_qty * move.product_uos_qty
            default_val = {
                'location_id': source_location.id,
                'product_qty': quantity,
                'product_uos_qty': uos_qty,
                'state': move.state,
                'scrapped': True,
                'location_dest_id': location_id,
                'tracking_id': move.tracking_id.id,
                'prodlot_id': move.prodlot_id.id,
                # START OF stock_analytic_account
                'analytic_account_id': move.analytic_account_id.id,
                # ENF OF stock_analytic_account
            }
            new_move = self.copy(cr, uid, move.id, default_val)

            res += [new_move]
            product_obj = self.pool.get('product.product')
            for product in product_obj.browse(cr, uid, [move.product_id.id],
                                              context=context):
                if move.picking_id:
                    uom = product.uom_id.name if product.uom_id else ''
                    message = _("%s %s %s has been <b>moved to</b> scrap.") \
                        % (quantity, uom, product.name)
                    move.picking_id.message_post(body=message)

        self.action_done(cr, uid, res, context=context)
        return res

    def check_assign(self, cr, uid, ids, context=None):
        """ Checks the product type and accordingly writes the state.
        @return: No. of moves done
        """
        done = []
        count = 0
        pickings = {}
        if context is None:
            context = {}
        for move in self.browse(cr, uid, ids, context=context):
            if move.product_id.type == 'consu' or move.location_id.usage == 'supplier':
                if move.state in ('confirmed', 'waiting'):
                    done.append(move.id)
                pickings[move.picking_id.id] = 1
                continue
            if move.state in ('confirmed', 'waiting'):
                # Important: we must pass lock=True to _product_reserve() to avoid race conditions and double reservations
                if move.analytic_reserved:
                    analytic_account_id = move.analytic_account_id.id
                else:
                    analytic_account_id = False
                res = self.pool.get(
                    'stock.location')._product_reserve(
                    cr, uid, [move.location_id.id], move.product_id.id,
                    move.product_qty, {'uom': move.product_uom.id,
                                       'analytic_account_id':
                                           analytic_account_id}, lock=True)
                if res:
                    #_product_available_test depends on the next status for correct functioning
                    #the test does not work correctly if the same product occurs multiple times
                    #in the same order. This is e.g. the case when using the button 'split in two' of
                    #the stock outgoing form
                    self.write(cr, uid, [move.id], {'state':'assigned'})
                    done.append(move.id)
                    pickings[move.picking_id.id] = 1
                    r = res.pop(0)
                    product_uos_qty = self.pool.get('stock.move').onchange_quantity(cr, uid, [move.id], move.product_id.id, r[0], move.product_id.uom_id.id, move.product_id.uos_id.id)['value']['product_uos_qty']
                    cr.execute('update stock_move set location_id=%s, product_qty=%s, product_uos_qty=%s where id=%s', (r[1], r[0],product_uos_qty, move.id))

                    while res:
                        r = res.pop(0)
                        product_uos_qty = self.pool.get('stock.move').onchange_quantity(cr, uid, [move.id], move.product_id.id, r[0], move.product_id.uom_id.id, move.product_id.uos_id.id)['value']['product_uos_qty']
                        move_id = self.copy(cr, uid, move.id, {'product_uos_qty': product_uos_qty, 'product_qty': r[0], 'location_id': r[1]})
                        done.append(move_id)
        if done:
            count += len(done)
            self.write(cr, uid, done, {'state': 'assigned'})

        if count:
            for pick_id in pickings:
                wf_service = netsvc.LocalService("workflow")
                wf_service.trg_write(uid, 'stock.picking', pick_id, cr)
        return count
