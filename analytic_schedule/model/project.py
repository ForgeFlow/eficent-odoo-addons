# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class Project(models.Model):
    _inherit = "project.project"

    @api.model
    def _compute_scheduled_dates(self):
        project_ids = self.search([('analytic_account_id', '=',
                                    self.analytic_account_id.id)])
        project_start_dates = []
        project_end_dates = []
        min_start_date_project = False
        max_end_date_project = False
        for project in project_ids:
            if project.date_start:
                project_start_dates.append(project.date_start)
            if project.date:
                project_end_dates.append(project.date)
        if project_start_dates:
            min_start_date_project = min(project_start_dates)
        if project_end_dates:
            max_end_date_project = max(project_end_dates)
        vals1 = {
            'date_start': min_start_date_project,
            'date': max_end_date_project,
        }
        self.analytic_account_id.write(vals1)
        return True

    @api.model
    def create(self, vals):
        acc = super(Project, self).create(vals)
        self._compute_scheduled_dates()
        return acc

    @api.multi
    def write(self, vals):
        res = super(Project, self).write(vals)
        if 'date_start' in vals or 'date' in vals:
            self._compute_scheduled_dates()
        return res
