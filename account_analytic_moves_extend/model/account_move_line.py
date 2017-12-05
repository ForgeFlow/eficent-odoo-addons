# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.multi
    def create_analytic_lines(self):
        for obj_line in self:
            # Only create analytic line if the associated account is
            # Expense or Income.
            if obj_line.account_id.user_type_id.name and\
                    obj_line.account_id.user_type_id.type in ('Income',
                                                              'Expenses'):
                if obj_line.analytic_account_id:
                    if obj_line.analytic_line_ids:
                        super(AccountMoveLine, self).create_analytic_lines()
        return True
