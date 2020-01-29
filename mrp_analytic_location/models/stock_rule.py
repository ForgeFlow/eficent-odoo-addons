from odoo import api, models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _prepare_mo_vals(
        self,
        product_id,
        product_qty,
        product_uom,
        location_id,
        name,
        origin,
        values,
        bom,
    ):
        res = super(StockRule, self)._prepare_mo_vals(
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            values,
            bom,
        )
        if location_id.analytic_account_id:
            res.update(
                {"analytic_account_id": location_id.analytic_account_id.id}
            )
        return res

    @api.multi
    def _run_buy(
        self,
        product_id,
        product_qty,
        product_uom,
        location_id,
        name,
        origin,
        values,
    ):
        if location_id.analytic_account_id:
            values.update(
                {"analytic_account_id": location_id.analytic_account_id.id}
            )
        return super(StockRule, self)._run_buy(
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            values,
        )

    @api.model
    def _prepare_purchase_request(self, origin, values):
        res = super(StockRule, self)._prepare_purchase_request(origin, values)
        res.update(
            {"analytic_account_id": values.get("analytic_account_id", False),}
        )
        return res

    @api.model
    def _prepare_purchase_request_line(
        self, request_id, product_id, product_qty, product_uom, values
    ):
        res = super(StockRule, self)._prepare_purchase_request_line(
            request_id, product_id, product_qty, product_uom, values
        )
        res.update(
            {"analytic_account_id": values.get("analytic_account_id", False),}
        )
        return res
