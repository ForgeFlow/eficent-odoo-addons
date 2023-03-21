# Copyright 2015-17 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    carrier_id = fields.Many2one(
        "delivery.carrier",
        "Delivery Method",
        help="""Complete this field if you plan to invoice the shipping based
            on picking.""",
    )
    carrier_in_po = fields.Boolean(compute="_compute_carrier_in_po")

    def _compute_carrier_in_po(self):
        for rec in self:
            rec.carrier_in_po = False
            for line in rec.order_line:
                if line.carrier_line:
                    rec.carrier_in_po = True

    @api.onchange("partner_id", "company_id")
    def onchange_partner_id(self):
        self.carrier_id = self.partner_id.property_delivery_carrier_id.id

    @api.model
    def _prepare_picking(self):
        result = super(PurchaseOrder, self)._prepare_picking()
        result.update({"carrier_id": self.carrier_id.id})
        return result

    def _prepare_invoice_line_from_carrier(self, carrier, price_unit):
        if self.carrier_in_po:
            return {}
        taxes = carrier.product_id.supplier_taxes_id
        invoice_line_tax_ids = self.fiscal_position_id.map_tax(taxes)
        invoice_line = self.env["account.invoice.line"]

        journal_domain = [
            ("type", "=", "purchase"),
            ("company_id", "=", self.company_id.id),
            ("currency_id", "=", self.partner_id.property_purchase_currency_id.id),
        ]
        default_journal_id = self.env["account.journal"].search(journal_domain, limit=1)
        data = {
            "name": carrier.name,
            "origin": self.origin,
            "uom_id": carrier.product_id.uom_id.id,
            "product_id": carrier.product_id.id,
            "account_id": invoice_line.with_context(
                {"journal_id": default_journal_id.id, "type": "in_invoice"}
            )._default_account(),
            "price_unit": price_unit,
            "quantity": 1.0,
            "discount": 0.0,
            "account_analytic_id": self.project_id.id,
            "invoice_line_tax_ids": invoice_line_tax_ids.ids,
        }
        account = invoice_line.get_invoice_line_account(
            "in_invoice",
            carrier.product_id,
            self.fiscal_position_id,
            self.env.user.company_id,
        )
        if account:
            data["account_id"] = account.id
        return data

    def _prepare_purchase_order_line(self):
        carrier = self.carrier_id
        final_price = carrier.get_price_available(self)
        vals = {
            "name": carrier.product_id.name,
            "order_id": self.id,
            "product_uom_qty": carrier.product_id.uom_id.id,
            "product_id": carrier.product_id.id,
            "price_unit": final_price,
            "carrier_line": True,
            "date_planned": datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            "product_uom": carrier.product_id.uom_po_id.id,
            "product_qty": 1.0,
        }
        return vals

    def _create_delivery_line(self):
        po_line_obj = self.env["purchase.order.line"]
        po_line_data = self._prepare_purchase_order_line()
        po_line_obj.create(po_line_data)

    def delivery_set(self):
        for order in self:
            if order.carrier_in_po:
                # do not create line if already exist
                return
            carrier = order.carrier_id
            if carrier:
                order._create_delivery_line()

            else:
                raise UserError(_("No carrier set for this order."))

        return True


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    carrier_line = fields.Boolean("This line is a carrier line", default=False)
