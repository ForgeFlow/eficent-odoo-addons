# -*- coding: utf-8 -*-
# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo import fields, models


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    internal_comments = fields.Text(
        string='Internal Comments',
        help="These comments will be propagated to the Purchase Order. "
             "Text introduced here is internal and merely informative."
    )
