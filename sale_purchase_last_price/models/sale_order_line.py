# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp.osv import fields, orm
import openerp.addons.decimal_precision as dp


class SaleOrderLine(orm.Model):
    _inherit = 'sale.order.line'

    def _get_last_purchase(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        """ Get last purchase price, last purchase date and last supplier """
        for so_line in self.browse(cr, uid, ids, context):
            po_line_ids = self.pool.get('purchase.order.line').search(
                cr, uid, [('product_id', '=', so_line.product_id.id),
                          ('date_order', '<=', so_line.order_id.date_order),
                          ('state', 'in', ['confirmed', 'done'])],
                order='id DESC', limit=1)
            res[so_line.id] = {}
            if po_line_ids:
                po_lines = self.pool.get(
                    'purchase.order.line').browse(
                    cr, uid, po_line_ids, context)
                res[so_line.id]['last_purchase_date'] = \
                    po_lines[0].date_order
                res[so_line.id]['last_purchase_price'] = \
                    po_lines[0].price_unit
                res[so_line.id]['last_supplier_id'] = \
                    po_lines[0].order_id.partner_id.id
        return res

    _columns = {
        'last_purchase_price': fields.function(
            fnct=_get_last_purchase,
            type='float', digits_compute=dp.get_precision('Product'),
            string='Last Purchase Price', store=True, required=False,
            multi=True, method=True),
        'last_purchase_date': fields.function(
            fnct=_get_last_purchase, string='Last Purchase Date',
            type='date', store=True, multi=True, method=True, required=False),
        'last_supplier_id': fields.function(
            fnct=_get_last_purchase, relation='res.partner',
            string='Last Supplier', type='many2one', store=True,
            multi=True, method=True, required=False)
    }

    _defaults = {
        'last_purchase_price': 0.0
    }
