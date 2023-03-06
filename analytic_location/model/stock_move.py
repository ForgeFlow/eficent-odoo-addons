# Copyright 2015-19 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _default_analytic_account_id(self):
        picking_type_id = self.picking_id._context.get("default_picking_type_id")
        if not picking_type_id:
            return False
        analytic_account = self.env["account.analytic.account"].search(
            [
                "|",
                ("picking_type_id", "=", picking_type_id),
                ("picking_type_out_id", "=", picking_type_id),
                ("parent_id", "=", 1),
            ]
        )
        if len(analytic_account):
            return analytic_account[0].id
        return False

    analytic_account_id = fields.Many2one(default=_default_analytic_account_id)
