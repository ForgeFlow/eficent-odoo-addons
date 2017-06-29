# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models
from openerp.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def create(self, vals):
        src_loc = self.env['stock.location'].browse(
            vals['location_id'])
        dest_loc = self.env['stock.location'].browse(
            vals['location_dest_id'])
        add_analytic_id = False
        if src_loc.analytic_account_id and dest_loc.analytic_account_id:
            if (src_loc.usage == 'customer'and dest_loc.usage ==
                'internal') or (src_loc.usage == 'internal' and
                   dest_loc.usage == 'customer'):
                add_analytic_id = dest_loc.analytic_account_id.id
        if src_loc.analytic_account_id and not dest_loc.analytic_account_id:
            if ((src_loc.usage == 'internal' and
                dest_loc.usage != 'internal')) or (
                (src_loc.usage == 'customer' and
                 dest_loc.usage == 'internal')):
                add_analytic_id = src_loc.analytic_account_id.id
        if not src_loc.analytic_account_id and dest_loc.analytic_account_id:
            if src_loc.usage == 'supplier':
                add_analytic_id = dest_loc.analytic_account_id.id
            if dest_loc.usage == 'customer' and src_loc != 'customer':
                add_analytic_id = dest_loc.analytic_account_id.id
            if src_loc.usage in ('inventory', 'customer') and \
                 dest_loc.usage == 'internal':
                add_analytic_id = dest_loc.analytic_account_id.id
        if add_analytic_id:
            vals['analytic_account_id'] = add_analytic_id
        return super(StockMove, self).create(vals)

    @api.multi
    def write(self, vals):
        check_analytic = False
        for move in self:
            if 'location_id' in vals:
                src_loc = self.env['stock.location'].browse([vals['location_id']])[0]
                check_analytic = True
            else:
                src_loc = move.location_id

            if 'location_dest_id' in vals:
                dest_loc = self.env['stock.location'].browse(
                    [vals['location_dest_id']])[0]
                check_analytic = True
            else:
                dest_loc = move.location_dest_id

            if check_analytic:
                add_analytic_id = False
                if src_loc.analytic_account_id and \
                        dest_loc.analytic_account_id:
                    if (src_loc.usage == 'customer' and dest_loc.usage ==
                        'internal') or (src_loc.usage == 'internal' and
                                                dest_loc.usage == 'customer'):
                        add_analytic_id = dest_loc.analytic_account_id.id
                if src_loc.analytic_account_id and not \
                        dest_loc.analytic_account_id:
                    if ((src_loc.usage == 'internal' and
                                 dest_loc.usage != 'internal')) or (
                            (src_loc.usage == 'customer' and
                                     dest_loc.usage == 'internal')):
                        add_analytic_id = src_loc.analytic_account_id.id
                if not src_loc.analytic_account_id and \
                        dest_loc.analytic_account_id:
                    if src_loc.usage == 'supplier':
                        add_analytic_id = dest_loc.analytic_account_id.id
                    if dest_loc.usage == 'customer' and src_loc != 'customer':
                        add_analytic_id = dest_loc.analytic_account_id.id
                    if src_loc.usage in ('inventory', 'customer') and \
                                    dest_loc.usage == 'internal':
                        add_analytic_id = dest_loc.analytic_account_id.id
                if add_analytic_id:
                    vals['analytic_account_id'] = add_analytic_id
        return super(StockMove, self).write(vals)

    @api.multi
    @api.constrains('location_id', 'location_dest_id')
    def _check_analytic_account(self):
        for move in self:
            if move.location_id and move.location_dest_id:
                if move.location_id.analytic_account_id and \
                        move.location_dest_id.analytic_account_id:
                    if move.location_id.analytic_account_id.id != \
                            move.location_dest_id.analytic_account_id.id:
                        raise ValidationError("Cannot move between different "
                                              "projects locations, please move"
                                              " first to general stock")
        return True
