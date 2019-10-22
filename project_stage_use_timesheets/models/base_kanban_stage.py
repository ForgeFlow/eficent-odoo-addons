# © 2015-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class BaseKanbanStage(models.Model):
    _inherit = "base.kanban.stage"

    allow_timesheets = fields.Boolean(
        "Timesheets",
        default=True,
        help="Check this field if setting this stage should make the project"
        " to manage timesheets",
    )
