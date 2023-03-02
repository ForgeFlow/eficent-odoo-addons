# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, exceptions, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    product_id = fields.Many2one(
        comodel_name='product.product', string='Product', required=True)

    @api.multi
    @api.constrains('product_id')
    def _check_is_employee(self):
        for rec in self:
            if not rec.product_id.is_employee:
                raise exceptions.ValidationError(
                    "The product is not marked as employee")
