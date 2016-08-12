# -*- coding: utf-8 -*-
# © 2015 Akretion, Benoît GUILLOT
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class PickingForceCurrencyRate(models.TransientModel):
    _name = "picking.force.currency.rate"
    _description = "Picking force currency rate"

    @api.model
    def _get_currency_rate(self):
        rate = 1
        if self.env.context.get('active_id', False):
            invoice = self.env['stock.picking'].browse(
                    self.env.context.get('active_id'))
            rate = invoice.currency_id.rate
        return rate

    currency_rate = fields.Float('Forced currency rate',
                                 help="You can force the currency rate on "
                                      "the picking with this field.",
                                 default=_get_currency_rate)

    @api.multi
    def force_currency_rate(self):
        for rec in self:
            if not self.env.context.get('active_id', False):
                continue
            picking = self.env['stock.picking'].browse(
                    self.env.context['active_id'])
            picking.currency_rate = rec.currency_rate
            # Recompute the price unit of the stock move according to the
            # original purchase unit price and the newly entered exchange rate.
            for move in picking.move_lines:
                if not move.purchase_line_id:
                    continue
                if move.purchase_line_id.order_id.currency_id == \
                        move.purchase_line_id.order_id.company_id.currency_id:
                    continue
                order_line = move.purchase_line_id
                order = order_line.order_id
                price_unit = order_line.price_unit
                if order_line.product_uom.id != \
                        order_line.product_id.uom_id.id:
                    price_unit *= order_line.product_uom.factor / \
                                  order_line.product_id.uom_id.factor
                currency = order.currency_id.with_context(
                    force_currency_rate=picking.currency_rate)
                move.price_unit = currency.compute(
                    price_unit, order.company_id.currency_id, round=False)
        return {'type': 'ir.actions.act_window_close'}
