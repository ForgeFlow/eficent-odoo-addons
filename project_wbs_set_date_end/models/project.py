# -*- coding: utf-8 -*-
# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class Project(models.Model):
    _inherit = "project.project"

    @api.multi
    def write(self, values):
        res = super(Project, self).write(values)
        if not self.date and 'date' not in values:
            self.date = self.date_start
        return res

    @api.model
    def create(self, values):
        if not values.get('date', False):
            values['date'] = values.get('date_start', False)
        return super(Project, self).create(values)
