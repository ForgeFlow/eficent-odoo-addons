# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
#        <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    @api.onchange('purchase_id')
    def purchase_order_change(self):
        new_lines = self.env['account.invoice.line']
        if not self.purchase_id.carrier_id:
            return super(AccountInvoice, self).purchase_order_change()
        data = self._add_delivery_cost_to_invoice()
        new_line = new_lines.new(data)
        new_line._set_additional_fields(self)
        self.invoice_line_ids += new_line
        res = super(AccountInvoice, self).purchase_order_change()
        seq = len(self.invoice_line_ids)
        self.invoice_line_ids[0].sequence = seq
        return res

    @api.multi
    def _add_delivery_cost_to_invoice(self):
        self.ensure_one()
        purchase_order = self.purchase_id
        if purchase_order:
            price_unit = purchase_order.carrier_id.get_price_available(
                purchase_order)
            return purchase_order._prepare_invoice_line_from_carrier(
                purchase_order.carrier_id,
                price_unit)
