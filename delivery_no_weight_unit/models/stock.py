# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
#        <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    weight_uom_id = fields.Many2one(
        'product.uom',
        'Unit of Measure',
        required=False,
        readonly=True,
        help="Unit of measurement for Weight",
        default=False
    )


class StockMove(models.Model):
    _inherit = 'stock.move'

    weight_uom_id = fields.Many2one(
        'product.uom',
        'Unit of Measure',
        required=False,
        readonly=True,
        help="Unit of measurement for Weight",
        default=False
    )
