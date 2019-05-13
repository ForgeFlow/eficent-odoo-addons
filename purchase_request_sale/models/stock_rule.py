# Copyright 2015-19 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


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
                    and sol.product_qty == product_qty:
                res['sale_order_line_id'] = sol.id
                res['name'] = group.name
                res['sequence'] = sol.sequence
                # The user who requested the PR will be the same as the SO,
                # otherwise the user will be Odoobot because of the pull rule
                res['requested_by'] = sol.order_id.user_id.id
                break
        return res

    @api.model
    def _prepare_purchase_request(self, origin, values):
        self.ensure_one()
        res = super(StockRule, self)._prepare_purchase_request(origin, values)
        if res.get('group_id'):
            group = self.env['procurement.group'].browse(
                res.get('group_id'))
            sales = group.sale_id
            res['sale_order_ids'] = [(4, sid.id) for sid in sales]
            # The user who requested the PR will be the same as the SO,
            # otherwise the user will be Odoobot because of the pull rule
            res['requested_by'] = sales.user_id.id
        else:
            res['sale_order_ids'] = \
                [(4, sid.id) for sid in
                 [self.group_id.mapped('sale_id')]]
        return res
