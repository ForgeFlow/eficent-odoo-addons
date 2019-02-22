# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    purchase_request_ids = fields.Many2many(
        comodel_name='purchase.request',
        relation='purchase_request_sale_rel',
        column1='request_id',
        column2='sale_id',
        string="Purchase Requests")

    @api.multi
    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        for sale in self:
            request_ids = sale.purchase_request_ids.filtered(
                lambda s: s.state in ['draft', 'to_approve'])
            if request_ids:
                request_ids.button_rejected()
            for request in request_ids:
                message = _(
                    'Purchase Request %s has been cancelled due to cancel of '
                    'the corresponding Sales Order %s') % (request.name,
                                                           sale.name)
                request.message_post(body=message)
        return res
