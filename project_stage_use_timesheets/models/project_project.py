# © 2015-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    @api.multi
    def write(self, values):
        if (
            values.get("stage_id")
            and self.env["base.kanban.stage"]
            .browse(values.get("stage_id"))
            .allow_timesheets
            and self.analytic_account_id.account_class == "work_package"
        ):
            values["allow_timesheets"] = True
        if (
            values.get("stage_id")
            and not self.env["base.kanban.stage"]
            .browse(values.get("stage_id"))
            .allow_timesheets
        ):
            values["allow_timesheets"] = False
        return super(ProjectProject, self).write(values)
