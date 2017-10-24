# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    delivery_line = fields.Boolean('Delivery order line', default=False)

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
