# Copyright 2014-17 ForgeFlow S.L.
#        <contact@forgeflow.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class ProjectProgressMeasurement(models.Model):
    _name = "project.progress.measurement"
    _description = "Project Progress Measurement"
    _inherit = "progress.measurement"

    project_id = fields.Many2one(
        "project.project", "Project", ondelete="cascade", index=True, required=True
    )

    _sql_constraints = [
        (
            "project_meas_type_date_uniq",
            "unique(project_id, " "progress_measurement_type, communication_date)",
            _(
                """Only one measurement of the same type can exist for each project
         on a given date."""
            ),
        )
    ]
