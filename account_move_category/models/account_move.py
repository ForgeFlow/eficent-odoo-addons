# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    category = fields.Selection(
        [('normal', 'Normal'),
         ('open', 'Opening Fiscal year'),
         ('close', 'Closing Fiscal Year')], 'Category', index=True)
