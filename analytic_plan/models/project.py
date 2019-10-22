# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Project(models.Model):
    _inherit = 'project.project'

    active_analytic_planning_version = fields.Many2one(
        related='analytic_account_id.active_analytic_planning_version',
        readonly=False,
    )
