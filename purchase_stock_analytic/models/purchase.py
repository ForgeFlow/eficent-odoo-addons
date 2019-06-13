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
                aa = line.account_analytic_id
                if len(res):
                    res[0].update({
                        'analytic_account_id': aa.id,
                        'location_dest_id': aa.location_id.id
                    })
                    picking.location_dest_id = aa.location_id.id
        return res

    @api.constrains('location_dest_id', 'account_analytic_id')
    @api.multi
    def _check_line_locations(self):
        # check users dont buy for projects to a generic location
        for rec in self:
            if rec.location_dest_id:
                if (rec.location_dest_id.analytic_account_id.id not in
                        rec.account_analytic_id.get_parents()):
                    print(rec.order_id.name)
                    print(rec.location_dest_id.analytic_account_id.id)
                    raise exceptions.ValidationError(
                        _('The location is not dedicated to project %s'
                          % rec.account_analytic_id.name))
        return True

    @api.onchange('account_analytic_id')
    def onchange_analytic(self):
        if self.account_analytic_id:
            self.location_dest_id = self.account_analytic_id.location_id
        else:
            self.location_dest_id = False

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
