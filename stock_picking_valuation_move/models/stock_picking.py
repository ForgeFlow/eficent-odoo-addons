# -*- coding: utf-8 -*-
# Copyright 2012 Andrea Cometa
# Copyright 2013 Agile Business Group sagl
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    account_move = fields.Many2one('account.move', 'Valuation Move',
                                   compute='compute_valuation_move')

    @api.multi
    def compute_valuation_move(self):
        account_move = self.env['account.move'].search(
            [('ref', '=', self.name)], limit=1)
        self.account_move = account_move
