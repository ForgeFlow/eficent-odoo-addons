# -*- coding: utf-8 -*-
from odoo import fields, models


class Project(models.Model):

    _inherit = 'project.project'

    stage_id = fields.Many2one(
        'analytic.account.stage',
        related='analytic_account_id.stage_id'
    )
