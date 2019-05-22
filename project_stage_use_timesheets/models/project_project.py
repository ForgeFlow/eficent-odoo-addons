# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.multi
    def write(self, values):
        for project in self:
            if values.get('stage_id', False):
                stage_obj = self.env['project.project.stage']
                stage = stage_obj.browse(values['stage_id'])
                if stage.allow_timesheets and project.account_class == \
                        'work_package':
                    values['allow_timesheets'] = True
                elif not stage.allow_timesheets:
                    values['allow_timesheets'] = False
        return super(ProjectProject, self).write(values)
