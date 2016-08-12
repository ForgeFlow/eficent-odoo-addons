# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.one
    def _show_force_currency(self):
        if self.state not in ['done', 'cancel']:
            if self.currency_id == self.company_id.currency_id:
                self.show_force_currency = False
            else:
                self.show_force_currency = True
        else:
            self.show_force_currency = False

    currency_rate = fields.Float('Forced currency rate',
                                 help="You can force the currency rate on the "
                                      "stock picking with this field.",
                                 readonly=True)

    currency_id = fields.Many2one('res.currency', string='Currency',
                                  readonly=True)

    show_force_currency = fields.Boolean(compute="_show_force_currency",
                                         string="Show force currency")

    @api.model
    def _get_invoice_vals(self, key, inv_type, journal_id, move):
        res = super(StockPicking, self)._get_invoice_vals(key,
                                                          inv_type,
                                                          journal_id, move)

        if move.picking_id and move.picking_id.currency_rate:
            res['currency_rate'] = move.picking_id.currency_rate
        return res


class StockMove(models.Model):

    _inherit = "stock.move"

    @api.model
    def get_price_unit(self, move):
        """ Returns the unit price to store on the quant """
        price_unit = super(StockMove, self).get_price_unit(move)
        if (
            move.picking_id and move.picking_id.currency_rate and
                move.purchase_line_id and
                move.purchase_line_id.order_id.currency_id !=
                move.purchase_line_id.order_id.company_id.currency_id
        ):
            currency = move.purchase_line_id.order_id.currency_id\
                .with_context(
                    force_currency_rate=move.picking_id.currency_rate)
            order_line = move.purchase_line_id
            price_unit = order_line.price_unit
            if order_line.product_uom.id != order_line.product_id.uom_id.id:
                price_unit *= order_line.product_uom.factor / \
                              order_line.product_id.uom_id.factor
            price_unit = currency.compute(
                    price_unit,
                    order_line.order_id.company_id.currency_id)
        return price_unit

