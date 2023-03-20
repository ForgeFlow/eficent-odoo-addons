# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def create(self, vals):
        src_loc = self.location_id.browse(vals['location_id'])
        dest_loc = self.location_id.browse(vals['location_dest_id'])
        add_analytic_id = False

        if src_loc.analytic_account_id and not dest_loc.analytic_account_id:
            add_analytic_id = src_loc.analytic_account_id.id

        if dest_loc.analytic_account_id and not src_loc.analytic_account_id:
            add_analytic_id = dest_loc.analytic_account_id.id
        if add_analytic_id:
            vals['analytic_account_id'] = add_analytic_id
        return super(StockMove, self).create(vals)

    @api.multi
    def write(self, vals):
        for move in self:
            if 'location_id' in vals:
                src_loc =\
                    self.env['stock.location'].browse(vals['location_id'])[0]
            else:
                src_loc = move.location_id

            if 'location_dest_id' in vals:
                dest_loc = self.env['stock.location'
                                    ].browse(vals['location_dest_id'])[0]
            else:
                dest_loc = move.location_dest_id

            if 'location_id' in vals or 'location_dest_id' in vals:
                add_analytic_id = False
                if src_loc.analytic_account_id and not \
                        dest_loc.analytic_account_id:
                    add_analytic_id = src_loc.analytic_account_id.id

                if dest_loc.analytic_account_id and not \
                        src_loc.analytic_account_id:
                    add_analytic_id = dest_loc.analytic_account_id.id
                if add_analytic_id:
                    vals['analytic_account_id'] = add_analytic_id
        return super(StockMove, self).write(vals)
