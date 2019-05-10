# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _prepare_supplierinfo(self, product_tmp):
        res = {
            'name': product_tmp.manufacturer.id,
            'product_name': product_tmp.manufacturer_pname,
            'product_code': product_tmp.manufacturer_pref,
            'sequence': 99,
            'min_qty': 0.0,
            'product_tmpl_id': product_tmp.id,
            'type': 'supplier'
        }
        return res

    @api.model
    def create(self, vals):
        product_tmp = super(ProductTemplate, self).create(vals)
        if 'manufacturer' in vals and vals['manufacturer']:
            supplierinfo_obj = self.env['product.supplierinfo']
            supplierinfo_vals = self._prepare_supplierinfo(product_tmp)
            supplierinfo_obj.create(supplierinfo_vals)
        return product_tmp

    @api.multi
    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        supplierinfo_obj = self.env['product.supplierinfo']
        for product in self:
            if 'manufacturer' in vals and vals['manufacturer']:
                supp_ids = supplierinfo_obj.search([
                    ('product_id', '=', product.id),
                    ('name', '=', vals['manufacturer'])])
                if not supp_ids:
                    supplierinfo_vals = self._prepare_supplierinfo(product)
                    supplierinfo_obj.create(supplierinfo_vals)
        return res
