# -*- coding: utf-8 -*-
# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo import api, models


class PurchaseRequestLineMakePurchaseOrder(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order"

    @api.multi
    def make_purchase_order(self):
        res = super(PurchaseRequestLineMakePurchaseOrder,
                    self).make_purchase_order()
        for po_id in set(res.get('domain')[0][2]):
            purchase = self.env['purchase.order'].browse(po_id)
            po_comment = purchase.internal_comments
            purchase_requests = self.item_ids.mapped('request_id')
            for pr in purchase_requests:
                if pr.internal_comments:
                    if not po_comment:
                        po_comment = "Purchase Request [%s]: %s" % (
                            pr.name, pr.internal_comments)
                    else:
                        po_comment = "%s\nPurchase Request [%s]: %s" % (
                            po_comment, pr.name, pr.internal_comments)
            purchase.internal_comments = po_comment
        return res
