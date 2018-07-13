# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _prepare_pack_ops(self, quants, forced_qties):
        res = super(StockPicking, self)._prepare_pack_ops(
            quants, forced_qties)
        return res
