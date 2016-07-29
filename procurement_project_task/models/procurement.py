# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models


class ProcurementOrder(models.Model):
    _inherit = "procurement.order"

    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Project Task',
        copy=True)

    @api.onchange('task_id')
    def _onchange_task_id(self):
        if self.task_id:
            self.project_id = self.task_id.project_id
            self.analytic_account_id = \
                self.task_id.project_id.analytic_account_id
