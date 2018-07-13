# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    @api.depends('order_line.account_analytic_id')
    def _compute_check_analytic_id(self):
        for po in self:
            if all(line.account_analytic_id for line in po.order_line):
                po.check_analytic_id = True
            else:
                po.check_analytic_id = False

    check_analytic_id = fields.Boolean(
        'Check Account Analytic',
        compute='_compute_check_analytic_id',
        store=True
    )
