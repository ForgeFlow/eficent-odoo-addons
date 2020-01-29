from odoo import _, exceptions, api, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.onchange("analytic_account_id", "location_src_id", "location_dest_id")
    def onchange_analytic(self):
        for mnf in self:
            if mnf.analytic_account_id:
                if mnf.analytic_account_id.location_id:
                    location = mnf.analytic_account_id.location_id
                    if not location:
                        location = env["stock.location"].search(
                            [
                                (
                                    "analytic_account_id",
                                    "=",
                                    mnf.analytic_account_id.id,
                                )
                            ]
                        )
                    if not location:
                        raise exceptions.UserError(
                            _(
                                "Please create or assign  a location for the "
                                "analytic account"
                            )
                        )
                    mnf.location_src_id = location
                    mnf.location_dest_id = location
        return True
