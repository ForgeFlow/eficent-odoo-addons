# -*- coding: utf-8 -*-
# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    internal_comments = fields.Text(
        string='Internal Comments',
        help="These comments come from the Purchase Request and are "
             "internal and merely informative."
    )
