# © 2023 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    picking_type_id = fields.Many2one(related="analytic_account_id.picking_type_id")
    location_id = fields.Many2one(
        related="analytic_account_id.location_id", readonly=True
    )
    dest_address_id = fields.Many2one(related="analytic_account_id.dest_address_id")
