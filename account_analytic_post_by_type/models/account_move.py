# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.multi
    def create_analytic_lines(self):
        new_lines = self.env['account.move.line']
        valid_list = ['Income', 'Expense', 'Cost', 'Revenue']
        for line in self:
            for valid in valid_list:
                if (line.account_id and
                        valid in line.account_id.user_type_id.name):
                    new_lines += line
                    break
        return super(AccountMoveLine, new_lines).create_analytic_lines()
