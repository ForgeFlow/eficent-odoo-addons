from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    active_analytic_planning_version = fields.Many2one(
        'account.analytic.plan.version',
        'Active planning Version',
        related='analytic_account_id.active_analytic_planning_version'
    )
