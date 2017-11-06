# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
#        <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def do_transfer(self):
        self.ensure_one()
        res = super(StockPicking, self).do_transfer()
        if self.purchase_id.order_line.filtered(lambda p: p.delivery_line):
            return res
        self._add_delivery_cost_to_po()
        return res

    @api.multi
    def _add_delivery_cost_to_po(self):
        self.ensure_one()
        purchase_order = self.purchase_id
        if purchase_order:
            price_unit = self.env['delivery.carrier'].get_price_available(
                purchase_order)
            purchase_order._create_delivery_line(self.purchase_id,
                                                 self.carrier_id, price_unit)
