# Copyright 2017 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def create_analytic_lines(self):
        new_lines = self.env["account.move.line"]
        valid_list = ["Income", "Expense", "Cost", "Revenue"]
        for line in self:
            for valid in valid_list:
                if line.account_id and valid in line.account_id.user_type_id.name:
                    new_lines += line
                    break
        return super(AccountMoveLine, new_lines).create_analytic_lines()
