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


class StockMove(orm.Model):

    _inherit = "stock.move"

    _columns = {        
        'analytic_account_id': fields.many2one('account.analytic.account',
                                               'Analytic Account'),
        'analytic_reserved': fields.boolean(
            'Reserved',
            help="Reserved for the Analytic Account"),
        'analytic_account_user_id': fields.related(
            'analytic_account_id', 'user_id', type='many2one',
            relation='res.users', string='Project Manager', store=True,
            readonly=True),
    }

    def _get_analytic_reserved(self, cr, uid, vals, context=None):
        context = context or {}
        analytic_obj = self.pool['account.analytic.account']
        aaid = vals['analytic_account_id']
        if aaid:
            aa = analytic_obj.browse(cr, uid, aaid, context=context)
            vals['analytic_reserved'] = aa.use_reserved_stock
        else:
            vals['analytic_reserved'] = False
        return vals

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


class StockInventoryLine(orm.Model):
    _inherit = "stock.inventory.line"

    _columns = {
        'analytic_account_id': fields.many2one('account.analytic.account',
                                               'Analytic Account'),
    }

    def _check_inventory_line(self, cr, uid, ids, context=None):
        """Refuse to record duplicate inventory lines
        Inventory lines with the sale Product, Location, Serial Number,
        Analytic Account and date are not taken into account correctly when
        computing the stock level difference, so we'll simply refuse to
        record them rather than allow users to introduce errors without
        even knowing it."""
        for line in self.browse(cr, uid, ids, context=context):
            inv_lines = self.search(
                cr, uid, [
                    ('product_id', '=', line.product_id.id),
                    ('location_id', '=', line.location_id.id),
                    ('prod_lot_id', '=', (
                        line.prod_lot_id
                        and line.prod_lot_id.id
                        or False)),
                    ('inventory_id.date', '=', line.inventory_id.date),
                    ('analytic_account_id', '=', line.analytic_account_id.id),
                    ('id', 'not in', ids),
                ], context=context)
            if inv_lines:
                raise orm.except_orm(
                    _('Duplicate line detected'),
                    _('You cannot enter more than a single inventory line for '
                      'the same Product, Location, Serial Number, Analytic '
                      'Account and date : \n'
                      '- Product: %s\n'
                      '- Location: %s\n'
                      '- Serial Number: %s\n'
                      '- Analytic Account: %s.') % (
                        line.product_id.default_code,
                        line.location_id.name,
                        (line.prod_lot_id and line.prod_lot_id.id or _('N/A')),
                        (line.analytic_account_id and
                         line.analytic_account_id.name or _('N/A')))
                )
        return True

    _constraints = [
        (_check_inventory_line, 'Duplicate line detected',
         ['location_id', 'product_id', 'prod_lot_id', 'analytic_account_id'])
    ]


class StockInventory(orm.Model):
    _inherit = "stock.inventory"

    def _inventory_line_hook(self, cr, uid, inventory_line, move_vals):
        """ Creates a stock move from an inventory line
        @param inventory_line:
        @param move_vals:
        @return:
        """
        if inventory_line.analytic_account_id:
            move_vals['analytic_account_id'] = \
                inventory_line.analytic_account_id.id
        return super(StockInventory, self)._inventory_line_hook(
            cr, uid, inventory_line, move_vals)

    def action_confirm(self, cr, uid, ids, context=None):
        """ Confirm the inventory and writes its finished date
        Attention!!! This method overrides the standard without calling Super
        The changes introduced by this module are encoded within a
        comments START OF and END OF stock_analytic_account.
        @return: True
        """
        if context is None:
            context = {}
        # to perform the correct inventory corrections we need analyze
        # stock location by
        # location, never recursively, so we use a special context
        product_context = dict(context, compute_child=False)

        location_obj = self.pool.get('stock.location')
        for inv in self.browse(cr, uid, ids, context=context):
            move_ids = []
            for line in inv.inventory_line_id:
                pid = line.product_id.id
                # START OF stock_analytic_account
                # Replace the existing entry:
                # product_context.update(uom=line.product_uom.id,
                # to_date=inv.date,
                # date=inv.date, prodlot_id=line.prod_lot_id.id)
                # ,with this one:
                product_context.update(
                    uom=line.product_uom.id, to_date=inv.date, date=inv.date,
                    prodlot_id=line.prod_lot_id.id,
                    analytic_account_id=line.analytic_account_id.id,)
                # ENF OF stock_analytic_account
                amount = location_obj._product_get(
                    cr, uid, line.location_id.id, [pid], product_context)[pid]
                change = line.product_qty - amount
                lot_id = line.prod_lot_id.id
                analytic_account_id = line.analytic_account_id.id or False
                if change:
                    location_id = line.product_id.property_stock_inventory.id
                    value = {
                        'name': _('INV:') + (line.inventory_id.name or ''),
                        'product_id': line.product_id.id,
                        'product_uom': line.product_uom.id,
                        'prodlot_id': lot_id,
                        'analytic_account_id': analytic_account_id,
                        'date': inv.date,
                    }

                    if change > 0:
                        value.update({
                            'product_qty': change,
                            'location_id': location_id,
                            'location_dest_id': line.location_id.id,
                        })
                    else:
                        value.update({
                            'product_qty': -change,
                            'location_id': line.location_id.id,
                            'location_dest_id': location_id,
                        })
                    move_ids.append(self._inventory_line_hook(cr, uid, line,
                                                              value))
            self.write(cr, uid, [inv.id], {'state': 'confirm',
                                           'move_ids': [(6, 0, move_ids)]})
            self.pool.get('stock.move').action_confirm(cr, uid, move_ids,
                                                       context=context)
        return True
