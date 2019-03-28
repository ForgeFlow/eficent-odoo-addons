# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
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

    def _prepare_invoice_line_from_carrier(self, carrier, price_unit):

        taxes = carrier.product_id.supplier_taxes_id
        invoice_line_tax_ids = self.fiscal_position_id.map_tax(taxes)
        invoice_line = self.env['account.invoice.line']

        journal_domain = [
            ('type', '=', 'purchase'),
            ('company_id', '=', self.company_id.id),
            ('currency_id', '=',
             self.partner_id.property_purchase_currency_id.id),
        ]
        default_journal_id = self.env['account.journal'].search(journal_domain,
                                                                limit=1)
        data = {
            'name': carrier.name,
            'origin': self.origin,
            'uom_id': carrier.product_id.uom_id.id,
            'product_id': carrier.product_id.id,
            'account_id': invoice_line.with_context(
                {'journal_id': default_journal_id.id,
                 'type': 'in_invoice'})._default_account(),
            'price_unit': price_unit,
            'quantity': 1.0,
            'discount': 0.0,
            'account_analytic_id': self.project_id.id,
            'invoice_line_tax_ids': invoice_line_tax_ids.ids
        }
        account = invoice_line.get_invoice_line_account(
            'in_invoice',
            carrier.product_id,
            self.fiscal_position_id,
            self.env.user.company_id)
        if account:
            data['account_id'] = account.id
        return data
