# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lpgl.html).

from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    check_number = fields.Integer(string="Check Number", readonly=True)
