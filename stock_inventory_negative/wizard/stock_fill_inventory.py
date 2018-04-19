# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, osv, orm


class StockFillInventory(orm.TransientModel):
    _inherit = "stock.fill.inventory"

    _columns = {
        'only_negative': fields.boolean('Only negative stock', required=False)
    }

    _defaults = {
        'only_negative': False,
    }

    def fill_inventory(self, cr, uid, ids, context=None):
        res = super(StockFillInventory, self).fill_inventory(
            cr, uid, ids, context)
        if self.browse(cr, uid, ids[0], context=context).only_negative:
            for line_id in self.pool.get('stock.inventory.line').search(
                    cr, uid, [('inventory_id', '=', context['active_ids'][0])]):
                line = self.pool.get('stock.inventory.line').browse(
                    cr, uid, line_id)
                if line.product_qty >= 0.0:
                    line.unlink()
        return res
