# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
#        <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    carrier_id = fields.Many2one(
        "delivery.carrier",
        "Delivery Method",
        help="""Complete this field if you plan to invoice the shipping based
            on picking."""
    )

    @api.onchange('partner_id', 'company_id')
    def onchange_partner_id(self):
        self.carrier_id = self.partner_id.property_delivery_carrier_id.id

    @api.model
    def _prepare_picking(self):
        result = super(PurchaseOrder, self)._prepare_picking()
        result.update({
            'carrier_id': self.carrier_id.id
        })
        return result

    @api.multi
    def delivery_set(self):
        for order in self:
            carrier = order.carrier_id
            src_address_id = order.partner_id
            dest_address_id = order.dest_address_id or False
            if (not dest_address_id and order.picking_type_id.warehouse_id and
                    order.picking_type_id.warehouse_id.partner_id):
                dest_address_id = order.picking_type_id.warehouse_id.partner_id
            if not dest_address_id:
                raise ValidationError(_('''
                    No destination address available! An address must be added
                    to the purchase order or the warehouse.'''))
            grid_id = carrier.grid_src_dest_get(src_address_id.id,
                                                dest_address_id.id)
            if not grid_id:
                raise ValidationError(_('''No Grid Available! No grid matching
                    for this carrier!.'''))

            if order.state not in ('draft', 'sent'):
                raise ValidationError(_('''
                    Order not in Draft State! The order state have to be
                    draft to add delivery lines.'''))
            price_unit = grid_id.get_price_available(order)
            self._create_delivery_line(order, grid_id, price_unit)
        return True

    def _create_delivery_line(self, order, grid_id, price_unit):
        PurchaseOrderLine = self.env['purchase.order.line']

        taxes = grid_id.product_id.taxes_id.\
            filtered(lambda t: t.company_id.id == grid_id.company_id.id)
        taxes_ids = taxes.ids
        if self.partner_id and self.fiscal_position_id:
            taxes_ids = self.fiscal_position_id.\
                map_tax(taxes, grid_id.product_id, self.partner_id).ids
        # create the purchase order line
        values = {
            'order_id': order.id,
            'name': grid_id.name,
            'product_qty': 1,
            'product_uom': grid_id.product_id.uom_id.id,
            'product_id': grid_id.product_id.id,
            'price_unit': price_unit,
            'taxes_id': [(6, 0, taxes_ids)],
            'date_planned': order.date_order,
        }
        if self.order_line:
            values['sequence'] = self.order_line[-1].sequence + 1
        pol = PurchaseOrderLine.sudo().create(values)
        return pol


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.multi
    def _prepare_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        if self.order_id.picking_type_id.warehouse_id and not\
                self.order_id.dest_address_id:
            if not self.order_id.picking_type_id.warehouse_id.partner_id:
                raise ValidationError(_('''Error! The warehouse must have an
                address.'''))
        if res:
            res[0]['partner_id'] = self.order_id.picking_type_id.warehouse_id.\
                partner_id.id or False
        return res
