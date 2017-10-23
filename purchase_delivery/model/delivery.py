# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
#        <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError


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

    @api.multi
    def grid_src_dest_get(self, src_id, dest_id):
        dest = self.env['res.partner'].browse(dest_id)
        src = self.env['res.partner'].browse(src_id)
        for carrier in self:
            get_id = lambda x: x.id
            country_ids = map(get_id, carrier.country_ids)
            state_ids = map(get_id, carrier.state_ids)
            src_country_ids = map(get_id, carrier.src_country_ids)
            src_state_ids = map(get_id, carrier.src_state_ids)
            if country_ids and dest.country_id.id not in country_ids:
                continue
            if state_ids and dest.state_id.id not in state_ids:
                continue
            if carrier.zip_from and (dest.zip or '') < carrier.zip_from:
                continue
            if carrier.zip_to and (dest.zip or '') > carrier.zip_to:
                continue
            if src_country_ids and src.country_id.id not in \
                    src_country_ids:
                continue
            if src_state_ids and src.state_id.id not in src_state_ids:
                continue
            if carrier.src_zip_from and (src.zip or '') < carrier.src_zip_from:
                continue
            if carrier.src_zip_to and (src.zip or '') > carrier.src_zip_to:
                continue
        return carrier

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
        self.ensure_one()
        total = weight = volume = quantity = 0
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
        price = 0.0
        criteria_found = False
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
                criteria_found = True
                break
        if not criteria_found:
            raise UserError(_("""Selected product in the delivery method
                doesn't fulfill any of the delivery carrier(s) criteria."""))
        return price
