# Copyright 2014-17 Eficent Business and IT Consulting Services S.L.
# Copyright 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.model
    def _default_dest_address(self):
        partner_id = self.env.context.get('partner_id', False)
        if partner_id:
            return self.env['res.partner'].address_get(
                [partner_id], ['delivery']
            )['delivery'],
        else:
            return False

    location_id = fields.Many2one(
        'stock.location',
        'Default Stock Location',
        domain=[('usage', '<>', 'view')]
    )
    dest_address_id = fields.Many2one(
        'res.partner',
        'Delivery Address',
        default=_default_dest_address,
        help="""Delivery address for the current contract project."""
    )


    @api.model
    def _prepare_location_vals(self, aa):
        analytic_account = aa
        vals = {
            "analytic_account_id": analytic_account.id,
            "name": analytic_account.name,
            "location_id": self.env.ref('stock.stock_location_stock').location_id.id,
            "usage": "internal",
        }
        return vals

    @api.model
    def _create_project_location(self, aa):
        if not aa.parent_id.location_id:
            vals = self._prepare_location_vals(aa)
            return self.env["stock.location"].create(vals)
        else:
            return aa.parent_id.location_id

    @api.model
    def create(self, vals):
        res = super(AccountAnalyticAccount, self).create(vals)
        loc = self._create_project_location(res)
        res["location_id"] = loc.id
        if vals.get('partner_id', False):
            res['dest_address_id'] = vals.get('partner_id')
        return res
