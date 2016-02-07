# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm, fields


class Product(orm.Model):
    _inherit = "product.product"

    def _prepare_supplierinfo(self, cr, uid, product_id, context=None):
        if context is None:
            context = {}
        product = self.pool['product.product'].browse(cr, uid, product_id,
                                                      context=context)
        res = {
            'name': product.manufacturer.id,
            'product_name': product.manufacturer_pname,
            'product_code': product.manufacturer_pref,
            'sequence': 99,
            'min_qty': 1,
            'product_id': product.id
        }
        return res

    def create(self, cr, uid, vals, context=None):
        product_id = super(Product, self).create(cr, uid, vals,
                                                 context=context)
        if 'manufacturer' in vals and vals['manufacturer']:
            supplierinfo_obj = self.pool['product.supplierinfo']
            supplierinfo_vals = self._prepare_supplierinfo(
                cr, uid, product_id, context=context)
            supplierinfo_obj.create(cr, uid, supplierinfo_vals,
                                    context=context)
        return product_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(Product, self).write(cr, uid, ids, vals, context=context)
        supplierinfo_obj = self.pool['product.supplierinfo']
        for product in self.browse(cr, uid, ids, context=context):
            if 'manufacturer' in vals and vals['manufacturer']:
                supp_ids = supplierinfo_obj.search(
                    cr, uid, [('product_id', '=', product.id),
                              ('name', '=', vals['manufacturer'])],
                    context=context)
                if not supp_ids:
                    supplierinfo_vals = self._prepare_supplierinfo(
                        cr, uid, product.id, context=context)
                    supplierinfo_obj.create(cr, uid, supplierinfo_vals,
                                            context=context)
        return res
