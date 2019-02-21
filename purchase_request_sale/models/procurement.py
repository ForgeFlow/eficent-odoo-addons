# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    def _prepare_purchase_request_line(self):
        res = super(ProcurementOrder, self)._prepare_purchase_request_line()
        for procurement in self:
            procs = procurement.group_id.procurement_ids.filtered(
                lambda p: (p.id != procurement.id and
                           p.product_id == procurement.product_id and
                           p.date_planned == procurement.date_planned and
                           p.warehouse_id == procurement.warehouse_id
                           ))
            sale_line = procs.mapped('sale_line_id')
            if len(sale_line) == 1:
                res['sale_order_line_id'] = sale_line.id
                res['name'] = procurement.name
                res['sequence'] = sale_line.sequence

        return res

    def _prepare_purchase_request(self):
        res = super(ProcurementOrder, self)._prepare_purchase_request()
        for procurement in self:
            procs = procurement.group_id.procurement_ids.filtered(
                lambda p: p.id != procurement.id)
            sales = procs.mapped('sale_line_id').mapped('order_id')
            res['sale_order_ids'] = [(4, sid.id) for sid in sales]
        return res

    def _search_existing_purchase_request(self):
        """This method is to be implemented by other modules that can
        provide a criteria to select the appropriate purchase request to be
        extended.
        """
        res = super(
            ProcurementOrder, self)._search_existing_purchase_request()
        for procurement in self:
            request_ids = procurement.group_id.procurement_ids.mapped(
                'request_id')
            if request_ids:
                return request_ids[0]
        return res
