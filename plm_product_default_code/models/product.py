# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, SUPERUSER_ID, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    default_code = fields.Char(string='Internal Reference',
                               related='product_variant_ids.default_code',
                               readonly=True)

    @api.multi
    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if 'engineering_code' in vals or 'engineering_revision' in vals:
            for pt in self:
                ecode = vals.get('engineering_code', pt.engineering_code)
                erev = vals.get('engineering_revision',
                                pt.engineering_revision)
                for pr in pt.product_variant_ids:
                    if erev > 0:
                        code = '%s - %s' % (ecode, erev)
                    else:
                        code = '%s' % ecode
                    pr.default_code = code
        return res


class ProductProduct(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char('Internal Reference', select=True,
                               readonly=True)

    @api.model
    def create(self, vals):
        if 'product_tmpl_id' in vals:
            pt = self.env['product.template'].browse(
                vals['product_tmpl_id'])
            if pt.engineering_revision > 0:
                code = '%s - %s' % (pt.engineering_code,
                                    pt.engineering_revision)
            else:
                code = '%s' % pt.engineering_code
            vals['default_code'] = code
        return super(ProductProduct, self).create(vals)

