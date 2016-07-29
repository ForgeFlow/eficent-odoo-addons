# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models


class ProcurementOrder(models.Model):
    _inherit = "procurement.order"

    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
        copy=True)

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id:
            self.analytic_account_id = self.project_id.analytic_account_id
        else:
            self.analytic_account_id = False
