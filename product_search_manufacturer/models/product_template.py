# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models
from openerp.exceptions import ValidationError, Warning
from openerp.tools.translate import _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        # Make a search with default criteria
        names1 = super(models.Model, self).name_search(
            name=name, args=args, operator=operator, limit=limit)
        # Make the other search
        names2 = []
        if name:
            domain = ['|', ('manufacturer_pname', '=ilike', name + '%'),
                      ('manufacturer_pref', '=ilike', name + '%')]
            names2 = self.search(
                domain, limit=limit).name_get()
        # Merge both results
        return list(set(names1) | set(names2))[:limit]
