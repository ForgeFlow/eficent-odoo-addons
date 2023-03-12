# Copyright 2015-17 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    manufacturer = fields.Many2one(
        "res.partner", "Manufacturer", domain=[("manufacturer", "=", True)]
    )
