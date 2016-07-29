# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models, _
from openerp.exceptions import UserError

class ProjectTask(models.Model):
    _inherit = 'project.task'

    wbs_element_id = fields.Many2one(
        comodel_name='project.wbs_element',
        string='WBS Element',
        copy=True
    )

    @api.onchange('wbs_element_id')
    def _onchange_wbs_element_id(self):
        if self.wbs_element_id:
            self.project_id = self.wbs_element_id.project_id

    @api.multi
    @api.constrains('wbs_element_id')
    def _check_wbs_element_assigned(self):
        for record in self:
            if record.wbs_element_id and record.wbs_element_id.child_ids:
                raise UserError(
                    _('A WBS Element that is parent of others cannot have '
                      'tasks assigned.'))
