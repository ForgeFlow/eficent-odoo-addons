# © 2015-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    @api.depends("stage_id", "stage_id.allow_timesheets")
    @api.multi
    def check_use_timesheets(self):
        for pp in self:
            if (
                pp.stage_id.allow_timesheets
                and pp.analytic_account_id.account_class == "work_package"
            ):
                self.allow_timesheets = True
            elif not pp.stage_id.allow_timesheets:
                self.allow_timesheets = False
