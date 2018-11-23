# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    purchase_request_ids = fields.One2many(
        'purchase.request', 'sale_order_id', 'Purchase Requests')

    @api.multi
    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        request_obj = self.env['purchase.request']
        for sale in self:
            request_ids = request_obj.search(
                [('sale_order_id', '=', sale.id),
                 ('state', 'in', ['draft', 'to_approve'])])
            if request_ids:
                request_ids.button_rejected()
            for request in request_ids:
                message = _(
                    'Purchase Request %s has been cancelled due to cancel of '
                    'the corresponding Sales Order %s') % (request.name,
                                                           sale.name)
                request.message_post(body=message)
        return res
