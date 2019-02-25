# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PurchaseRequest(models.Model):

    _inherit = "purchase.request"

    sale_order_ids = fields.Many2many(
        comodel_name='sale.order',
        relation='purchase_request_sale_rel',
        column1='sale_id',
        column2='request_id',
        string="Sales")


class PurchaseRequestLine(models.Model):

    _inherit = "purchase.request.line"

    sale_order_line_id = fields.Many2one(
        'sale.order.line', 'Sales Order Line', readonly=True)
