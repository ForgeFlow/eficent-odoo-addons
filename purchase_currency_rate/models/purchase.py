# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class PurchaseOrder(models.Model):

    _inherit = "purchase.order"

    @api.one
    def _show_force_currency(self):
        if self.state == 'draft':
            if self.currency_id.id == self.company_id.currency_id.id:
                self.show_force_currency = False
            else:
                self.show_force_currency = True
        else:
            self.show_force_currency = False

    currency_rate = fields.Float('Forced currency rate',
                                 help="You can force the currency rate on the "
                                      "purchase order with this field.",
                                 readonly=True)
    show_force_currency = fields.Boolean(compute="_show_force_currency",
                                         string="Show force currency")

    @api.model
    def _prepare_invoice(self, order, line_ids, context=None):
        res = super(PurchaseOrder, self)._prepare_invoice(order, line_ids)
        if order.currency_rate:
            res['currency_rate'] = order.currency_rate
        return res

    @api.model
    def _prepare_order_line_move(self, order, order_line, picking_id,
                                 group_id):
        if order.currency_rate:
            new_self = self.with_context(
                force_currency_rate=order.currency_rate)
        else:
            new_self = self
        return super(PurchaseOrder, new_self)._prepare_order_line_move(
                order, order_line, picking_id, group_id)

    @api.multi
    def action_picking_create(self):
        picking_id = super(PurchaseOrder, self).action_picking_create()
        picking = self.env['stock.picking'].browse(picking_id)
        for res in self:
            picking.currency_id = res.currency_id
            if res.currency_rate:
                picking.currency_rate = self.currency_rate
        return picking
