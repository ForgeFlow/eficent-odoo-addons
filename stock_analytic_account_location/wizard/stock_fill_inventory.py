# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm, osv
from openerp.tools.translate import _


class StockFillInventory(orm.Model):

    _inherit = "stock.fill.inventory"

    _columns = {
        'analytic_inventory': fields.boolean('Project Inventory'),
        'location_id': fields.many2one(
            'stock.location', 'Location',
            required=False)
    }

    def fill_inventory(self, cr, uid, ids, context=None):
        """ To Import stock inventory according to products available
        in the selected locations.
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param ids: the ID or list of IDs if we want more than one
        @param context: A standard dictionary
        @return:
        """
        if context is None:
            context = {}

        inventory_line_obj = self.pool.get('stock.inventory.line')
        location_obj = self.pool.get('stock.location')
        move_obj = self.pool.get('stock.move')
        uom_obj = self.pool.get('product.uom')
        if ids and len(ids):
            ids = ids[0]
        else:
            return {'type': 'ir.actions.act_window_close'}
        fill_inventory = self.browse(cr, uid, ids, context=context)

        if fill_inventory.recursive:
            location_ids = location_obj.search(
                cr, uid, [('location_id', 'child_of',
                           [fill_inventory.location_id.id])], order="id",
                context=context)
        else:
            location_ids = [fill_inventory.location_id.id]

        if fill_inventory.analytic_inventory:
            location_ids = location_obj.search(
                cr, uid, [('analytic_account_id', '=',
                           [fill_inventory.analytic_account_id.id])], order="id",
                context=context)
            analytic_account_id = fill_inventory.analytic_account_id.id
            if fill_inventory.recursive:
                children_loc = self.pool.get('stock.location')._get_sublocations(cr, uid, location_ids)
                location_ids.extend(children_loc)
            location_ids = list(set(location_ids))
        else:
            analytic_account_id = False

        res = {}
        flag = False

        for location in location_ids:
            datas = {}
            res[location] = {}
            search_criteria = ['|', ('location_dest_id', '=', location),
                               ('location_id', '=', location),
                               ('state', '=', 'done')]
            # if analytic_account_id:
            #     search_criteria.extend(
            #         [('analytic_account_id', '=', analytic_account_id)])

            move_ids = move_obj.search(cr, uid, search_criteria,
                                       context=context)
            local_context = dict(context)
            local_context['raise-exception'] = False
            for move in move_obj.browse(cr, uid, move_ids, context=context):
                lot_id = move.prodlot_id.id
                prod_id = move.product_id.id

                if move.location_dest_id.id != move.location_id.id:
                    if move.location_dest_id.id == location:
                        qty = uom_obj._compute_qty_obj(
                            cr, uid, move.product_uom, move.product_qty,
                            move.product_id.uom_id, context=local_context)
                    else:
                        qty = -uom_obj._compute_qty_obj(
                            cr, uid, move.product_uom, move.product_qty,
                            move.product_id.uom_id, context=local_context)

                    if datas.get((prod_id, lot_id, analytic_account_id)):
                        qty += datas[(prod_id, lot_id, analytic_account_id)][
                            'product_qty']

                    datas[(prod_id, lot_id, analytic_account_id)] = \
                        {'product_id': prod_id,
                         'location_id': location,
                         'product_qty': qty,
                         'product_uom': move.product_id.uom_id.id,
                         'prod_lot_id': lot_id,
                         'analytic_account_id': analytic_account_id}
            if datas:
                flag = True
                res[location] = datas

        if not flag:
            raise osv.except_osv(_('Warning!'),
                                 _('No product in this location. '
                                   'Please select a location in the '
                                   'product form.'))

        for stock_move in res.values():
            for stock_move_details in stock_move.values():
                stock_move_details.update(
                    {'inventory_id': context['active_ids'][0]})
                domain = []
                for field, value in stock_move_details.items():
                    if field == 'product_qty':
                        domain.append((field, 'in', [value, '0']))
                        continue
                    domain.append((field, '=', value))
                if fill_inventory.set_stock_zero:
                    stock_move_details.update({'product_qty': 0})

                line_ids = inventory_line_obj.search(cr, uid, domain,
                                                     context=context)

                if not line_ids:
                    inventory_line_obj.create(cr, uid, stock_move_details,
                                              context=context)
        return {'type': 'ir.actions.act_window_close'}
