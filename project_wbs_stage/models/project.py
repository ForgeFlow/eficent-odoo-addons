# Copyright 2017-19 Eficent Business and IT Consulting Services S.L.
# Copyright 2017-19 Luxim d.o.o.
# Copyright 2017-19 Matmoz d.o.o.
# Copyright 2017-19 Deneroteam.

# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Project(models.Model):

    _inherit = 'project.project'

    stage_id = fields.Many2one(
        'analytic.account.stage',
        related='analytic_account_id.stage_id'
    )
