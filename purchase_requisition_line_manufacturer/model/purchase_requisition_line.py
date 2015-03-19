# -*- encoding: utf-8 -*-
########################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
########################################################################

from openerp.osv import orm, fields
from openerp.tools.translate import _

class purchase_requisition_line(orm.Model):
    _inherit = "purchase.requisition.line"

    _columns = {
        'manufacturer': fields.many2one('res.partner', 'Manufacturer'),
        'manufacturer_pname': fields.char('Manufacturer Product Name',
                                          help="Manufacturer's Product Name"),
        'manufacturer_pref': fields.char('Manufacturer Product Code',
                                         help="Manufacturer's Product Code"),
    }

    def onchange_product_id(self, cr, uid, ids, product_id,
                            product_uom_id, context=None):
        context = context or {}
        product_obj = self.pool.get('product.product')
        res = super(purchase_requisition_line, self).onchange_product_id(
            cr, uid, ids, product_id, product_uom_id, context=context)
        res['value'].update({'manufacturer': False})
        if product_id:
            product = product_obj.browse(cr, uid, product_id, context=context)
            if product.manufacturer:
                res['value'].update({'manufacturer': product.manufacturer.id})
            res['value'].update(
                {'manufacturer_pref': product.manufacturer_pref})
            res['value'].update(
                {'manufacturer_pname': product.manufacturer_pname})
        return res

    def onchange_manufacturer(self, cr, uid, ids, product_id, manufacturer,
                              context=None):
        res = {}
        context = context or {}
        product_obj = self.pool.get('product.product')
        if product_id:
            product = product_obj.browse(cr, uid, product_id, context=context)
            if (
                product.manufacturer
                and product.manufacturer.id != manufacturer
            ):
                raise orm.except_orm(_('Invalid Action!'),
                                     _('The Manufacturer does not match with '
                                       ' that defined in the Product.'))
        return res

    def onchange_manufacturer_pname(self, cr, uid, ids, product_id,
                                    manufacturer_pname, context=None):
        res = {}
        context = context or {}
        product_obj = self.pool.get('product.product')
        if product_id:
            product = product_obj.browse(cr, uid, product_id, context=context)
            if product.manufacturer_pname != manufacturer_pname:
                raise orm.except_orm(_('Invalid Action!'),
                                     _('The Manufacturer Product Name does '
                                       'not match '
                                       'with that defined in the Product.'))
        else:
            if manufacturer_pname:
                product_ids = product_obj.search(
                    cr, uid, [('manufacturer_pname', '=', manufacturer_pname)],
                    context=context)
                if product_ids:
                    pr_id = product_ids[0]
                    product = product_obj.browse(cr, uid, pr_id,
                                                 context=context)
                    manufacturer_pref = product.manufacturer_pref
                    manufacturer = product.manufacturer.id
                else:
                    pr_id = False
                    manufacturer_pref = ''
                    manufacturer = False
                    msg = _('No suitable product was found for this '
                            'manufacturer part name. This item cannot not '
                            'be ordered unless the product is added.')

                    res['warning'] = {
                        'title': "Warning",
                        'message': msg,
                    }

                res['value'] = {
                    'product_id': pr_id,
                    'manufacturer_pref': manufacturer_pref,
                    'manufacturer': manufacturer,
                }
        return res

    def onchange_manufacturer_pref(self, cr, uid, ids, product_id,
                                   manufacturer_pref, context=None):
        res = {}
        context = context or {}
        product_obj = self.pool.get('product.product')
        if product_id:
            product = product_obj.browse(cr, uid, product_id, context=context)
            if product.manufacturer_pref != manufacturer_pref:
                raise orm.except_orm(_('Invalid Action!'),
                                     _('The Manufacturer Product Code does '
                                       'not match '
                                       'with that defined in the Product.'))
        else:
            if manufacturer_pref:
                product_ids = product_obj.search(
                    cr, uid, [('manufacturer_pref', '=', manufacturer_pref)],
                    context=context)
                if product_ids:
                    pr_id = product_ids[0]
                    product = product_obj.browse(cr, uid, pr_id,
                                                 context=context)
                    manufacturer_pname = product.manufacturer_pname
                    manufacturer = product.manufacturer.id
                else:
                    pr_id = False
                    manufacturer_pname = ''
                    manufacturer = False
                    msg = _('No suitable product was found for this '
                            'manufacturer part number. This item cannot not '
                            'be ordered unless the product is added.')

                    res['warning'] = {
                        'title': "Warning",
                        'message': msg,
                    }

                res['value'] = {
                    'product_id': pr_id,
                    'manufacturer_pname': manufacturer_pname,
                    'manufacturer': manufacturer,
                }

        return res
