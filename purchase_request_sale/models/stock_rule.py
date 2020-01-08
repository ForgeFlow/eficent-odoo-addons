# Copyright 2015-19 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class StockRule(models.Model):
    _inherit = 'stock.rule'

    @api.model
    def _prepare_purchase_request_line(self, request_id, product_id,
                                       product_qty, product_uom, values):
        res = super(StockRule, self)._prepare_purchase_request_line(
            request_id, product_id, product_qty, product_uom, values)

        group = values['group_id']
        sale_line = group.mapped('sale_id.order_line')
        for sol in sale_line:
            if sol.product_id == product_id and sol.product_uom == product_uom\
                    and sol.product_uom_qty == product_qty:
                res['sale_order_line_id'] = sol.id
                res['name'] = group.name
                # The user who requested the PR will be the same as the SO,
                # otherwise the user will be Odoobot because of the pull rule
                res['requested_by'] = sol.order_id.user_id.id
                break
        return res

    @api.model
    def _prepare_purchase_request(self, origin, values):
        res = super(StockRule, self)._prepare_purchase_request(origin, values)
        group = values.get('group_id')
        if group:
            sales = group.sale_id
            # The user who requested the PR will be the same as the SO,
            # otherwise the user will be Odoobot because of the pull rule
            res['requested_by'] = sales.user_id.id
            res['sale_order_ids'] = [(4, sid.id) for sid in sales]
        return res
