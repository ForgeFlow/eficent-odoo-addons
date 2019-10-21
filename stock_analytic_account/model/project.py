from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    move_ids = fields.One2many(
        related='analytic_account_id.move_ids'
    )
