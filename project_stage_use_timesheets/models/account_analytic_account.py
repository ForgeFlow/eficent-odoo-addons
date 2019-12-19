# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def write(self, values):
        if (
            values.get("stage_id")
            and self.env["analytic.account.stage"]
            .browse(values.get("stage_id"))
            .allow_timesheets
            and self.account_class == "work_package"
        ):
            self.project_ids.allow_timesheets = True
        if (
            values.get("stage_id")
            and not self.env["analytic.account.stage"]
            .browse(values.get("stage_id"))
            .allow_timesheets
        ):
            self.project_ids.allow_timesheets = False
        return super(AccountAnalyticAccount, self).write(values)
