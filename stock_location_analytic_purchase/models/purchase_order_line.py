# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, _
from odoo.exceptions import ValidationError


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
