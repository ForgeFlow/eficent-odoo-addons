# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PurchaseRequest(models.Model):

    _inherit = "purchase.request"

    sale_order_id = fields.Many2one(
        'sale.order', 'Sales Order', readonly=True)


class PurchaseRequestLine(models.Model):

    _inherit = "purchase.request.line"

    sale_order_line_id = fields.Many2one(
        'sale.order.line', 'Sales Order Line', readonly=True)
