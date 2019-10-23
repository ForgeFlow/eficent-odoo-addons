from odoo import _, api, exceptions, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.depends("analytic_account_id")
    def compute_project_location(self):
        for mnf in self:
            if mnf.analytic_account_id:
                if mnf.analytic_account_id.location_id:
                    mnf.location_src_id = mnf.analytic_account_id.location_id
                    mnf.location_dest_id = mnf.analytic_account_id.location_id
                else:
                    raise exceptions.ValidationError(
                        _(
                            "Please create or assign  a location for the "
                            "analytic account"
                        )
                    )
        return True

    location_src_id = fields.Many2one(compute=compute_project_location, store=True)
    location_dest_id = fields.Many2one(compute=compute_project_location, store=True)
