# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent (<http://www.eficent.com/>)
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
from openerp.osv import fields, orm
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _


class AnalyticResourcePlanLineProduce(orm.TransientModel):
    _name = "analytic.resource.plan.line.produce"
    _description = "Produce from Resource Plan Lines"

    _columns = {
        'item_ids': fields.one2many(
            'analytic.resource.plan.line.produce.item',
            'wiz_id', 'Items'),
    }

    def _prepare_item(self, cr, uid, line, context=None):
        return [{
            'product_id': line.product_id.id,
            'product_qty': line.unit_amount - line.qty_available,
            'product_uom_id': line.product_uom_id.id,
            'line_id': line.id,
        }]

    def default_get(self, cr, uid, fields, context=None):
        res = super(AnalyticResourcePlanLineProduce, self).default_get(
            cr, uid, fields, context=context)
        res_plan_obj = self.pool['analytic.resource.plan.line']
        resource_plan_line_ids = context.get('active_ids', [])
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

    def do_produce(self, cr, uid, ids, context=None):
        res = []
        res_plan_obj = self.pool['analytic.resource.plan.line']
        data = self.browse(cr, uid, ids[0], context=context)

        for item in data.item_ids:
            move_id = res_plan_obj.create_produce_move(
                cr, uid, item.line_id.id, item.product_qty, context=context)
            res.append(move_id)

        return {
            'domain': "[('id','in', ["+','.join(map(str, res))+"])]",
            'name': _('Stock Moves'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.move',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }


class AnalyticResourcePlanLineProduceItem(orm.TransientModel):
    _name = "analytic.resource.plan.line.produce.item"
    _description = "Resource plan produce item"

    _columns = {
        'wiz_id': fields.many2one(
            'analytic.resource.plan.line.produce',
            'Wizard', required=True, ondelete='cascade',
            readonly=True),
        'line_id': fields.many2one('analytic.resource.plan.line',
                                   'Resource Plan Line',
                                   required=True,
                                   readonly=True),
        'product_qty': fields.float(string='Quantity to produce',
                                    digits_compute=dp.get_precision(
                                        'Product UoS')),
        'product_uom_id': fields.related('line_id',
                                         'product_uom_id', type='many2one',
                                         relation='product.uom',
                                         string='UoM',
                                         readonly=True)
    }
