# Copyright 2014-17 Eficent Business and IT Consulting Services S.L.
# Copyright 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockQuant(models.Model):

    _inherit = "stock.quant"

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        related='location_id.analytic_account_id',
    )
