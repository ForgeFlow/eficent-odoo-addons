# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
#        <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    @api.multi
    def get_price(self):
        if self._context.get('purchase_order_id', False):
            self.price = 0.0

    @api.multi
    def name_get(self):
        if not len(self.ids):
            return []
        if self._context is None:
            self._context = {}
        return [(r['id'], r['name']) for r in self.read(['name'])]

    src_country_ids = fields.Many2many(
        'res.country',
        'delivery_grid_src_country_rel',
        'grid_id',
        'country_id',
        'Source Countries'
    )
    src_state_ids = fields.Many2many(
        'res.country.state',
        'delivery_grid_src_state_rel',
        'grid_id',
        'state_id',
        'Source States'
    )
    src_zip_from = fields.Char(
        'Start Source Zip',
        size=12
    )
    src_zip_to = fields.Char(
        'To Source Zip',
        size=12
    )

    @api.multi
    def get_price_available(self, order):
        weight = volume = quantity = 0
        total_delivery = 0.0
        for line in order.order_line:
            if not line.product_id:
                continue
            qty = line.product_uom._compute_quantity(line.product_qty,
                                                     line.product_id.uom_id)
            weight += (line.product_id.weight or 0.0) * qty
            volume += (line.product_id.volume or 0.0) * qty
            quantity += qty
        total = (order.amount_total or 0.0) - total_delivery
        total = order.currency_id.with_context(date=order.date_order).\
            compute(total, order.company_id.currency_id)

        return self.get_price_from_picking(total, weight, volume, quantity)

    def get_price_from_picking(self, total, weight, volume, quantity):
        if self.delivery_type == 'fixed':
            return self.fixed_price
        price = 0.0
        price_dict = {
            'price': total,
            'volume': volume,
            'weight': weight,
            'wv': volume * weight,
            'quantity': quantity
        }
        for line in self.price_rule_ids:
            test = safe_eval(line.variable + line.operator + str(line.max_value
                                                                 ), price_dict)
            if test:
                price = line.list_base_price + line.list_price * price_dict[
                    line.variable_factor]
        return price
