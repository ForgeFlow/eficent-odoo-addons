# Copyright 2014-17 ForgeFlow S.L.
# Copyright 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import time

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProgressMeasurement(models.Model):

    _name = "progress.measurement"
    _description = "Progress Measurement"

    @api.constrains("value", "progress_measurement_type")
    def _check_is_value_less_than_max(self):
        for item in self:
            if item.progress_measurement_type:
                if item.value > item.progress_measurement_type.default_max_value:
                    raise ValidationError(
                        _(
                            "Error! The value must be less than the maximum "
                            "permitted defined in the progress measurement type"
                        )
                    )

    name = fields.Char(
        "Description", size=32, required=False, help="Description given to the measure"
    )
    communication_date = fields.Date(
        required=True,
        help="Date when the measurement " "was communicated",
        default=time.strftime("%Y-%m-%d"),
    )
    communication_date_print = fields.Char("Communication Date", size=32, required=True)
    value = fields.Float(required=True, help="Value of the " "measure")
    progress_measurement_type = fields.Many2one(
        "progress.measurement.type", required=True
    )
    user_id = fields.Many2one(
        "res.users", "Entered by", required=True, default=lambda self: self.env.uid
    )

    @api.model
    def create(self, vals):
        vals["communication_date_print"] = vals["communication_date"]
        return super(ProgressMeasurement, self).create(vals)

    def write(self, vals):
        if "communication_date" in vals:
            vals["communication_date_print"] = vals["communication_date"]
        return super(ProgressMeasurement, self).write(vals)
