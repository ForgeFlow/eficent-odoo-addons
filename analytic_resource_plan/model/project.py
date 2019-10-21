from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    resource_count = fields.Integer(
        related='analytic_account_id.resource_count'
    )
