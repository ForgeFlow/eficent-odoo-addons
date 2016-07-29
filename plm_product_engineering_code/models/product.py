# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, SUPERUSER_ID, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    @api.depends('name', 'engineering_code', 'engineering_revision')
    def name_get(self):
        result = []
        for pt in self:
            if not pt.engineering_code:
                name = pt.name
            elif pt.engineering_revision > 0:
                name = '[%s - %s] %s' % (pt.engineering_code,
                                         pt.engineering_revision, pt.name)
            else:
                name = '[%s] %s ' % (pt.engineering_code, pt.name)
            result.append((pt.id, name))
        return result
