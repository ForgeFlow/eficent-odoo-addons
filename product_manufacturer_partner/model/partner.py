# Copyright 2015-17 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    manufacturer = fields.Boolean()
