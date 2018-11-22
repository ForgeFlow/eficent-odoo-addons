# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
##############################################################################

from odoo import api, models, fields, _
import odoo.addons.decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _get_last_purchase(self):
        """ Get last purchase price, last purchase date and last supplier """
        for so_line in self:
            po_lines = self.env['purchase.order.line'].search(
                [('product_id', '=', so_line.product_id.id),
                 ('date_order', '<=', so_line.order_id.date_order),
                 ('state', 'in', ['purchase', 'done'])],
                order='id DESC', limit=1)

            if po_lines:
                so_line.last_purchase_date = po_lines[0].date_order
                so_line.last_purchase_price = po_lines[0].price_unit
                so_line.last_supplier_id = po_lines[0].order_id.partner_id.id
            else:
                so_line.last_purchase_price = 0.0
                so_line.last_purchase_date = False
                so_line.last_supplier_id = False

    last_purchase_price = fields.Float(
        compute=_get_last_purchase,
        digits=dp.get_precision('Product'),
        string='Last Purchase Price')
    last_purchase_date = fields.Date(
        compute=_get_last_purchase, string='Last Purchase Date')
    last_supplier_id = fields.Many2one(
        compute=_get_last_purchase, comodel_name='res.partner',
        string='Last Supplier')
