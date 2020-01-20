from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    use_timesheet_validators = fields.Boolean(
        string="Timesheet validators",
        help="Only validators can validate timesheets",
    )
