# Copyright 2018 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lpgl.html).

from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    check_number = fields.Char(related="payment_id.check_number", store=True)
