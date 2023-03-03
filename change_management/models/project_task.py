# -*- coding: utf-8 -*-
# Copyright 2017 Matmoz d.o.o. (<http://www.matmoz.si>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    change_id = fields.Many2one(
        'change.management.change',
        'Action on Change',
        readonly=True,
        help="Task is an action on a change identified by this label."
    )


class ProjectProject(models.Model):
    _inherit = 'project.project'

    change_ids = fields.One2many(
        'change.management.change',
        'project_id',
        'Project changes'
    )

    change_count = fields.Integer(
        compute='_compute_change_count',
        type='integer'
    )

    @api.depends('change_ids')
    def _compute_change_count(self):
        for record in self:
            record.change_count = len(record.change_ids)

    @api.model
    def _get_alias_models(self):
        res = super(ProjectProject, self)._get_alias_models()
        res.append(("change.management.change", "Change Requests"))
        return res
