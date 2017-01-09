# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm
from openerp.tools import float_compare, float_round, DEFAULT_SERVER_DATETIME_FORMAT


class StockLocation(orm.Model):
    _inherit = "stock.location"

    def _product_value(self, cr, uid, ids, field_names, arg, context=None):
        res = super(StockLocation, self)._product_value(
            cr, uid, ids, field_names, arg, context)
        return res

    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'analytic_account_id': False,
        })
        return super(StockLocation, self).copy(cr, uid, id, default, context)


    def _product_reserve(self, cr, uid, ids, product_id, product_qty, context=None, lock=False):
        """
        Openerp standard to avoid stock_analytic_account _product_reserve
        to be called
        """
        result = []
        amount = 0.0
        if context is None:
            context = {}
        uom_obj = self.pool.get('product.uom')
        uom_rounding = self.pool.get('product.product').browse(cr, uid, product_id, context=context).uom_id.rounding
        if context.get('uom'):
            uom_rounding = uom_obj.browse(cr, uid, context.get('uom'), context=context).rounding

        locations_ids = self.search(cr, uid, [('location_id', 'child_of', ids)])
        if locations_ids:
            # Fetch only the locations in which this product has ever been processed (in or out)
            cr.execute("""SELECT l.id FROM stock_location l WHERE l.id in %s AND
                        EXISTS (SELECT 1 FROM stock_move m WHERE m.product_id = %s
                                AND ((state = 'done' AND m.location_dest_id = l.id)
                                    OR (state in ('done','assigned') AND m.location_id = l.id)))
                       """, (tuple(locations_ids), product_id,))
            locations_ids = [i for (i,) in cr.fetchall()]
        for id in locations_ids:
            if lock:
                try:
                    # Must lock with a separate select query because FOR UPDATE can't be used with
                    # aggregation/group by's (when individual rows aren't identifiable).
                    # We use a SAVEPOINT to be able to rollback this part of the transaction without
                    # failing the whole transaction in case the LOCK cannot be acquired.
                    cr.execute("SAVEPOINT stock_location_product_reserve")
                    cr.execute("""SELECT id FROM stock_move
                                  WHERE product_id=%s AND
                                          (
                                            (location_dest_id=%s AND
                                             location_id<>%s AND
                                             state='done')
                                            OR
                                            (location_id=%s AND
                                             location_dest_id<>%s AND
                                             state in ('done', 'assigned'))
                                          )
                                  FOR UPDATE of stock_move NOWAIT""", (product_id, id, id, id, id), log_exceptions=False)
                except Exception:
                    # Here it's likely that the FOR UPDATE NOWAIT failed to get the LOCK,
                    # so we ROLLBACK to the SAVEPOINT to restore the transaction to its earlier
                    # state, we return False as if the products were not available, and log it:
                    cr.execute("ROLLBACK TO stock_location_product_reserve")
                    _logger.warning("Failed attempt to reserve %s x product %s, likely due to another transaction already in progress. Next attempt is likely to work. Detailed error available at DEBUG level.", product_qty, product_id)
                    _logger.debug("Trace of the failed product reservation attempt: ", exc_info=True)
                    return False

            # XXX TODO: rewrite this with one single query, possibly even the quantity conversion
            cr.execute("""SELECT product_uom, sum(product_qty) AS product_qty
                          FROM stock_move
                          WHERE location_dest_id=%s AND
                                location_id<>%s AND
                                product_id=%s AND
                                state='done'
                          GROUP BY product_uom
                       """,
                       (id, id, product_id))
            results = cr.dictfetchall()
            cr.execute("""SELECT product_uom,-sum(product_qty) AS product_qty
                          FROM stock_move
                          WHERE location_id=%s AND
                                location_dest_id<>%s AND
                                product_id=%s AND
                                state in ('done', 'assigned')
                          GROUP BY product_uom
                       """,
                       (id, id, product_id))
            results += cr.dictfetchall()
            total = 0.0
            results2 = 0.0
            for r in results:
                amount = uom_obj._compute_qty(cr, uid, r['product_uom'], r['product_qty'], context.get('uom', False))
                results2 += amount
                total += amount
            if total <= 0.0:
                continue

            amount = results2
            compare_qty = float_compare(amount, 0, precision_rounding=uom_rounding)
            if compare_qty == 1:
                if amount > min(total, product_qty):
                    amount = min(product_qty, total)
                result.append((amount, id))
                product_qty -= amount
                total -= amount
                if product_qty <= 0.0:
                    return result
                if total <= 0.0:
                    continue
        return False


    _columns = {
        'analytic_account_id': fields.many2one('account.analytic.account',
                                               'Analytic Account'),
    }

    def _check_moves(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        location_obj = self.pool.get('stock.location')
        move_obj = self.pool.get('stock.move')
        uom_obj = self.pool.get('product.uom')
        for location_id in ids:
            children_loc = location_obj._get_sublocations(cr, uid, location_id)
            for loc_id in children_loc:
                location = self.browse(cr, uid, loc_id, context)
                datas = {}
                analytic_account_id = location.analytic_account_id
                search_criteria = ['|', ('location_dest_id', '=', location.id),
                                   ('location_id', '=', location.id),
                                   ('state', '=', 'done'),
                                   ('analytic_account_id', '!=', False)]


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
                        if qty != 0:
                            return False
        return True

    def _check_analytic_account(self, cr, uid, ids, context=None):
        for loc in self.browse(cr, uid, ids):
            if loc.analytic_account_id:
                analytic = loc.analytic_account_id
                if loc.location_id:
                    parent = loc.location_id
                    if parent.usage != 'view' \
                            and parent.analytic_account_id != analytic:
                        return False
        return True

    _constraints = [(_check_moves, "This location contains products of "
                                   "different projects, move them out first",
                     ['analytic_account_id']),
                    (_check_analytic_account, "Sublocations can only be related"
                                              " to the same project",
                    ['analytic_account_id'])]
