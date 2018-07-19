# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#  - Jordi Ballester Alomar
# Copyright 2017 MATMOZ d.o.o.
#  - Matjaž Mozetič
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, exceptions, api, models


class PurchaseOrderLine(models.Model):

    _inherit = "purchase.order.line"

    @api.multi
    def _prepare_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        for line in self:
            if line.account_analytic_id:
                res[0].update({
                    'analytic_account_id': line.account_analytic_id.id,
                    'location_dest_id':
                        line.account_analytic_id.location_id.id,
                })
        return res


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def _prepare_picking(self):
        res = super(PurchaseOrder, self)._prepare_picking()
        if self.project_id:
            res.update(
                {'location_dest_id': self.project_id.location_id.id, })
        return res

    @api.multi
    def button_confirm(self):
        for po in self:
            if (po.project_id and not
                    po.project_id.location_id):
                raise exceptions.ValidationError(_(
                    'Please assign a location for the project.'
                ))
        return super(PurchaseOrder, self).button_confirm()
