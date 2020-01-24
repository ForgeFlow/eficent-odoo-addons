# -*- coding: utf-8 -*-
# Copyright 2016-2017 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class StockChangeProductQty(models.TransientModel):
    _inherit = 'stock.change.product.qty'

    @api.model
    def _prepare_inventory(self, wizard, inventory_filter, line_data):
        res = super(StockChangeProductQty, self)._prepare_inventory(
            wizard, inventory_filter, line_data)
        if wizard.location_id and wizard.location_id.analytic_account_id:
            res.update(
                analytic_account_id=wizard.location_id.analytic_account_id.id)
        return res
