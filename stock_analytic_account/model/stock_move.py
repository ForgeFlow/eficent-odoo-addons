# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services S.L.
# Copyright 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, exceptions, fields, models


class StockMove(models.Model):

    _inherit = "stock.move"

    analytic_account_user_id = fields.Many2one(
        'res.users',
        related='analytic_account_id.partner_id.user_id',
        store=True,
        readonly=True
    )

    @api.multi
    @api.constrains('analytic_account_id', 'location_id', 'location_dest_id')
    def _check_analytic_account(self):
        for move in self:
            analytic = move.analytic_account_id
            src_anal = move.location_id.analytic_account_id
            dest_anal = move.location_dest_id.analytic_account_id
            if src_anal and dest_anal:
                raise exceptions.ValidationError(_("""
                    Cannot move between different projects locations,
                    please move first to general stock"""))
            elif src_anal and not dest_anal:
                if src_anal != analytic:
                    raise exceptions.ValidationError(_(
                        "Wrong analytic account in source or move"))
            elif dest_anal and not src_anal:
                if dest_anal != analytic:
                    raise exceptions.ValidationError(_(
                        "Wrong analytic account in destination or "
                        "move"))
        return True


class StockScrap(models.Model):

    _inherit = 'stock.scrap'

    def _prepare_move_values(self):
        values = super(StockScrap, self)._prepare_move_values()
        values.update({
            'analytic_account_id': self.move_id.analytic_account_id.id
        })
        return values
