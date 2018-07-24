# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.multi
    def _compute_valid_to_post(self):
        valid_list = ['Income', 'Expense', 'Cost', 'Revenue']
        for rec in self:
            if rec.analytic_account_id:
                for valid in valid_list:
                    if valid in rec.account_id.user_type_id.name:
                        rec.valid_to_post = True
                        return
            rec.valid_to_post = False

    valid_to_post = fields.Boolean(
        'Entry allowed to be post',
        compute='_compute_valid_to_post'
    )

    @api.multi
    def create_analytic_lines(self):
        new_lines = self.env['account.move.line']
        for line in self:
            if line.valid_to_post:
                new_lines += line
        return super(AccountMoveLine, new_lines).create_analytic_lines()
