# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    procurement_ids = fields.One2many(
        comodel_name='procurement.order',
        inverse_name='task_id',
        string='Procurement Orders',
        copy=False)


