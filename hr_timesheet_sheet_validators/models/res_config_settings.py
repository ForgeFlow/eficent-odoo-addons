# Copyright 2014-20 ForgeFlow S.L.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    use_timesheet_validators = fields.Boolean(
        related="company_id.use_timesheet_validators",
        readonly=False,
    )
