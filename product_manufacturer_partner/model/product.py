# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    manufacturer = fields.Many2one('res.partner', 'Manufacturer',
                                   domain=[('manufacturer', '=', True)])
