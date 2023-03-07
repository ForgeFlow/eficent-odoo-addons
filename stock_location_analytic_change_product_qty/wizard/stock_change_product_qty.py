# Copyright 2023 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockChangeProductQty(models.TransientModel):
    _inherit = "stock.change.product.qty"

    @api.depends("product_id")
    def _compute_analytic_account_id(self):
        for wiz in self:
            warehouse = self.env["stock.warehouse"].search(
                [("company_id", "=", self.env.company.id)], limit=1
            )
            if warehouse.lot_stock_id.analytic_account_id:
                wiz.analytic_account_id = warehouse.lot_stock_id.analytic_account_id.id
        return True

    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        compute=_compute_analytic_account_id,
        string="Analytic Account",
    )
