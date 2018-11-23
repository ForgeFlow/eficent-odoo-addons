# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    def _prepare_purchase_request_line(self):
        res = super(ProcurementOrder, self)._prepare_purchase_request_line()
        for procurement in self:
            sale_line = procurement.group_id.procurement_ids.filtered(
                lambda p: p.id != procurement.id).sale_line_id
            if len(sale_line) == 1:
                res['sale_order_line_id'] = sale_line.id
                res['name'] = procurement.name
                res['sequence'] = sale_line.sequence
        return res

    def _prepare_purchase_request(self):
        res = super(ProcurementOrder, self)._prepare_purchase_request()
        for procurement in self:
            sale_line = procurement.group_id.procurement_ids.filtered(
                lambda p: p.id != procurement.id).sale_line_id
            if len(sale_line) == 1:
                res['sale_order_id'] = sale_line.order_id.id
        return res

    def _search_existing_purchase_request(self):
        """This method is to be implemented by other modules that can
        provide a criteria to select the appropriate purchase request to be
        extended.
        """
        res = super(
            ProcurementOrder, self)._search_existing_purchase_request()
        purchase_request_obj = self.env['purchase.request']
        for procurement in self:
            if procurement.sale_line_id and \
                    procurement.sale_line_id.order_id:
                request_ids = purchase_request_obj.search(
                    [('sale_order_id', '=',
                      procurement.sale_line_id.order_id.id),
                     ('state', '=', 'draft')])
                if request_ids:
                    return request_ids[0]
        return res
