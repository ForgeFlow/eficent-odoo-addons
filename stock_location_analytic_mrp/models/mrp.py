# © 2023 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, exceptions, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.constrains("location_src_id", "location_dest_id")
    def _check_mrp_analytic_location(self):
        for mrp in self:
            if mrp.analytic_account_id:
                analytic = mrp.analytic_account_id
                if (
                    mrp.location_src_id.analytic_account_id != analytic
                    or mrp.location_dest_id.analytic_account_id != analytic
                ):
                    raise exceptions.ValidationError(
                        _(
                            "The production location does not belong to the "
                            "analytic account"
                        )
                    )

    @api.onchange("analytic_account_id")
    def onchange_analytic_account_id(self):
        for rmove in self.move_raw_ids:
            rmove.analytic_account_id = self.analytic_account_id
        for fmove in self.move_finished_ids:
            fmove.analytic_account_id = self.analytic_account_id
