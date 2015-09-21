# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.tools.translate import _
from openerp.osv import fields, orm
from openerp import netsvc
import openerp.addons.decimal_precision as dp


class AnalyticRPLChangeStockReservedQuantity(orm.TransientModel):
    _name = "analytic.rpl.change.stock.reserved.quantity"
    _description = "Resource plan change stock reserved quantity"

    _columns = {
        'item_ids': fields.one2many(
            'analytic.rpl.change.stock.reserved.quantity.item',
            'wiz_id', 'Items'),
    }

    def _prepare_item(self, cr, uid, item, context=None):
        return [{
            'line_id': item.line_id.id,
            'product_id': item.line_id.product_id.id,
            'product_qty': item.product_qty,
        }]

    def default_get(self, cr, uid, fields, context=None):
        res = super(AnalyticRPLChangeStockReservedQuantity, self).default_get(
            cr, uid, fields, context=context)
        res_plan_obj = self.pool['analytic.resource.plan.line']
        resource_plan_line_ids = context.get('actgve_ids', [])
        active_model = context.get('active_model')

        if not resource_plan_line_ids:
            return res
        assert active_model == 'analytic.resource.plan.line', \
            'Bad context propagation'

        items = []
        for line in res_plan_obj.browse(cr, uid, resource_plan_line_ids,
                                        context=context):
                items += self._prepare_item(cr, uid, line, context=context)
        res['item_ids'] = items
        return res

    def change_stock_reserved_quantity(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        change_reserved_quantity = self.browse(cr, uid, ids[0],
                                               context=context)
        line_plan_obj = self.pool.get('analytic.resource.plan.line')
        for item in change_reserved_quantity.item_ids:
            line = item.line_id
            if line.state != 'confirm':
                raise orm.except_orm(
                    _('Attention !'),
                    _('All resource plan lines must be '
                      'confirmed.'))
            line_plan_obj.change_reserved_stock_quantity(cr, uid, line,
                                                         item.product_qty,
                                                         context=None)
        return True


class AnalyticRPLChangeStockReservedQuantityItem(orm.TransientModel):
    _name = "analytic.rpl.change.stock.reserved.quantity.item"
    _description = "Resource plan change stock reserved quantity item"

    _columns = {
        'wiz_id': fields.many2one(
            'analytic.rpl.change.stock.reserved.quantity',
            'Wizard', required=True, ondelete='cascade',
            readonly=True),
        'line_id': fields.many2one('analytic.resource.plan.line',
                                   'Resource Plan Line',
                                   required=True,
                                   readonly=True),
        'product_id': fields.related('line_id', 'product_id', type='many2one',
                                     relation='product.product',
                                     string='Product',
                                     readonly=True),
        'product_qty': fields.float(string='New quantity',
                                    digits_compute=dp.get_precision(
                                        'Product UoS')),
    }
