# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#  - Jordi Ballester Alomar
# Copyright 2017 MATMOZ d.o.o.
#  - Matjaž Mozetič
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, exceptions, api, fields, models


class PurchaseOrderLine(models.Model):

    _inherit = "purchase.order.line"

    @api.model
    def _first_picking_copy_vals(self, key, lines):
        """The data to be copied to new pickings is updated with data from the
        grouping key.  This method is designed for extensibility, so that
        other modules can store more data based on new keys."""
        vals = super(PurchaseOrderLine, self)._first_picking_copy_vals(
            key, lines)
        for key_element in key:
            if 'account_analytic_id' in key_element.keys():
                vals['account_analytic_id'] = \
                    key_element['account_analytic_id'].id
        return vals

    @api.model
    def _get_group_keys(self, order, line, picking=False):
        """Define the key that will be used to group. The key should be
        defined as a tuple of dictionaries, with each element containing a
        dictionary element with the field that you want to group by. This
        method is designed for extensibility, so that other modules can add
        additional keys or replace them by others."""
        key = super(PurchaseOrderLine, self)._get_group_keys(order, line,
                                                             picking=picking)
        anal_id = line.account_analytic_id
        return key + ({'account_analytic_id': anal_id},)

    @api.multi
    def _prepare_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        for line in self:
            if line.account_analytic_id:
                res[0].update({
                    'analytic_account_id': line.account_analytic_id.id,
                    'location_dest_id':
                        line.account_analytic_id.location_id.id,
                    'picking_type_id':
                        line.account_analytic_id.picking_type_id.id
                })
                picking.location_dest_id = line.account_analytic_id.location_id.id
                picking.picking_type_id = line.account_analytic_id.picking_type_id.id
        return res

    picking_type_id = fields.Many2one(
        'stock.picking.type',
        'Default Picking Type for the receipt')


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def button_confirm(self):
        for po in self:
            if (po.project_id and not
                    po.project_id.location_id):
                raise exceptions.ValidationError(_(
                    'Please assign a location for the project.'
                ))
        return super(PurchaseOrder, self).button_confirm()
