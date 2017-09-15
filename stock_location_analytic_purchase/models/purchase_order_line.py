# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


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


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.multi
    @api.constrains('account_analytic_id')
    def _check_purchase_analytic(self):
        for line in self:
            picking_type = line.order_id.picking_type_id
            if picking_type:
                loc_analytic_account = picking_type.default_location_dest_id.\
                    analytic_account_id
            if line.account_analytic_id:
                if line.account_analytic_id != loc_analytic_account:
                    raise ValidationError(_('''The analytic account in the
                        destination location and in the PO line must match'''))
        return True
