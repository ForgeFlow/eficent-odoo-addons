# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models
from openerp.tools.translate import _
from openerp.exceptions import UserError


class Product(models.Model):
    _inherit = 'product.product'

    is_skill = fields.Boolean('Is a skill')
