# Copyright 2017-19 Eficent Business and IT Consulting Services S.L.
# Copyright 2017-19 Luxim d.o.o.
# Copyright 2017-19 Matmoz d.o.o.
# Copyright 2017-19 Deneroteam.

# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class Project(models.Model):
    _name = 'project.project'
    _inherit = ['project.project']

    stage_id = fields.Many2one(
        comodel_name='base.kanban.stage',
        related='analytic_account_id.stage_id',
        store=True
    )
