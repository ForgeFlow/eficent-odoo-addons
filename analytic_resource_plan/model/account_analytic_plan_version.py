# Copyright 2017 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class AccountAnalyticPlanVersion(models.Model):
    _inherit = "account.analytic.plan.version"

    default_resource_plan = fields.Boolean("Default for resource plan", default=False)

    @api.constrains("default_resource_plan")
    def _check_default_resource(self):
        for _rec in self:
            default_res_plan = self.search([("default_resource_plan", "=", True)])
            if len(default_res_plan) > 1:
                raise ValidationError(
                    _("Only one default for resource plan version can" " exist.")
                )
