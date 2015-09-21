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
from openerp.tools.translate import _


class AnalyticResourcePlanLine(orm.Model):
    
    _inherit = 'analytic.resource.plan.line'

    def _show_button_bom_explode(self, cr, uid, ids, field_names, arg,
                                 context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            if not line.bom_id:
                res[line.id] = False
            else:
                res[line.id] = True
        return res

    _columns = {
        'bom_id': fields.many2one('mrp.bom', 'Bill of Materials',
                                  readonly=True, required=False,
                                  states={'draft': [('readonly', False)]}),
        'show_button_bom_explode': fields.function(
            _show_button_bom_explode, type='boolean'),
    }

    def on_change_product_id(self, cr, uid, id, product_id, context=None):
        res = super(AnalyticResourcePlanLine, self).on_change_product_id(
            cr, uid, id, product_id, context=context)

        bom_obj = self.pool.get('mrp.bom')
        product = self.pool.get('product.product').browse(cr, uid, product_id,
                                                          context=context)
        bom_id = bom_obj._bom_find(cr, uid, product.id, product.uom_id and
                                   product.uom_id.id, [])
        if 'value' in res:
            res['value']['bom_id'] = bom_id
        return res

    def button_bom_explode_to_resource_plan(self, cr, uid, ids, context=None):
        res = self.bom_explode_to_resource_plan(cr, uid, ids, context=context)
        return {
            'domain': "[('id','in', ["+','.join(map(str, res))+"])]",
            'name': _('New Resource Plan Lines'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'analytic.resource.plan.line',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }

    def _prepare_resource_plan_line(self, cr, uid, plan, line, new_qty,
                                    context=None):
        product_obj = self.pool['product.product']
        bom_obj = self.pool['mrp.bom']
        product = product_obj.browse(cr, uid,
                                     line['product_id'],
                                     context=context)
        bom_id = bom_obj._bom_find(cr, uid, line['product_id'],
                                   line['product_uom'] and
                                   product.uom_id.id, [])
        return {
            'account_id': plan.account_id.id,
            'name': line['name'],
            'date': plan.date,
            'state': 'draft',
            'product_id': line['product_id'],
            'product_uom_id': line['product_uom'],
            'unit_amount': new_qty,
            'bom_id': bom_id,
            'parent_id': plan.id,
        }

    def bom_explode_to_resource_plan(self, cr, uid, ids, context=None):
        bom_obj = self.pool['mrp.bom']
        uom_obj = self.pool['product.uom']
        plan_line_obj = self.pool['analytic.resource.plan.line']
        res = []
        for plan in self.browse(cr, uid, ids, context=context):
                # Search for child resource plan lines.
                plan_line_ids = plan_line_obj.search(
                    cr, uid, [('parent_id', '=',
                               plan.id),
                              ('state', '=', 'draft')],
                    context=context)
                plan_line_obj.unlink(cr, uid, plan_line_ids,
                                     context=context)
                factor = uom_obj._compute_qty(
                    cr, uid, plan.product_uom_id.id,
                    plan.unit_amount,
                    plan.bom_id.product_uom.id)
                bom_res = bom_obj._bom_explode(
                    cr, uid, plan.bom_id,
                    factor / plan.bom_id.product_qty,
                    routing_id=False)
                components = bom_res[0]  # product_lines
                for line in components:
                    plan_line_ids = plan_line_obj.search(
                        cr, uid, [('parent_id', '=',
                                   plan.id),
                                  ('product_id', '=', line['product_id']),
                                  ('product_uom_id', '=',
                                   line['product_uom']),
                                  ('state', '!=', 'draft')],
                        context=context)
                    total_qty = 0.0
                    for plan_line in plan_line_obj.browse(cr, uid,
                                                          plan_line_ids,
                                                          context=context):
                        total_qty += plan_line.unit_amount

                    if line['product_qty'] > total_qty:
                        new_qty = line['product_qty'] - total_qty
                        resource_line_data = self._prepare_resource_plan_line(
                            cr, uid, plan, line, new_qty, context=context)
                        plan_id = plan_line_obj.create(cr, uid,
                                                       resource_line_data,
                                                       context=context)
                        res.append(plan_id)
        return res

    def _prepare_consume_move(self, cr, uid, line, product_qty, context=None):
        if line.product_id.type not in ('product', 'consu'):
            raise orm.except_orm(
                _('Error'),
                _('The product must be stockable or consumable.'))
        if product_qty <= 0:
            raise orm.except_orm(
                _('Error'),
                _('The quantity to consume must be greater or equal to 0.'))

        if line.state != 'confirm':
            raise orm.except_orm(
                _('Error'),
                _('The resource plan line must be confirmed.'))
        destination_location_id = line.product_id.property_stock_production.id
        if not line.account_id.location_id:
            raise orm.except_orm(
                _('Error'),
                _('The analytic account must contain a default Location.'))
        source_location_id = line.account_id.location_id.id
        move_data = {
            'name': line.name,
            'date': line.date,
            'product_id': line.product_id.id,
            'product_qty': product_qty,
            'product_uom': line.product_uom_id.id,
            'location_id': source_location_id,
            'location_dest_id': destination_location_id,
            'state': 'assigned',
            'company_id': line.account_id.company_id.id,
            'analytic_account_id': line.account_id.id,
        }
        return move_data

    def _create_stock_move(self, cr, uid, move_data, context=None):
        stock_move = self.pool['stock.move']
        return stock_move.create(cr, uid, move_data, context=context)

    def _complete_stock_move(self, cr, uid, move_id, context=None):
        stock_move = self.pool['stock.move']
        return stock_move.action_done(cr, uid, [move_id], context=context)

    def create_consume_move(self, cr, uid, line_id, product_qty, context=None):
        line = self.browse(cr, uid, line_id, context=context)
        move_data = self._prepare_consume_move(cr, uid, line,
                                               product_qty, context=context)
        move_id = False
        if move_data:
            move_id = self._create_stock_move(cr, uid, move_data,
                                              context=context)
            self._complete_stock_move(cr, uid, move_id, context=context)
        return move_id

    def _prepare_produce_move(self, cr, uid, line, product_qty, context=None):
        if line.product_id.type not in ('product', 'consu'):
            raise orm.except_orm(
                _('Error'),
                _('The product must be stockable or consumable.'))
        if product_qty <= 0:
            raise orm.except_orm(
                _('Error'),
                _('The quantity to produce must be greater or equal to 0.'))
        if line.state != 'confirm':
            raise orm.except_orm(
                _('Error'),
                _('The resource plan line must be confirmed.'))
        source_location_id = line.product_id.property_stock_production.id
        if not line.account_id.location_id:
            raise orm.except_orm(
                _('Error'),
                _('The analytic account must contain a default Location.'))
        destination_location_id = line.account_id.location_id.id
        move_data = {
            'name': line.name,
            'date': line.date,
            'product_id': line.product_id.id,
            'product_qty': product_qty,
            'product_uom': line.product_uom_id.id,
            'location_id': source_location_id,
            'location_dest_id': destination_location_id,
            'state': 'assigned',
            'company_id': line.account_id.company_id.id,
            'analytic_account_id': line.account_id.id,
        }
        return move_data

    def _create_produce_move(self, cr, uid, move_data, context=None):
        stock_move = self.pool['stock.move']
        return stock_move.create(cr, uid, move_data, context=context)

    def create_produce_move(self, cr, uid, line_id, product_qty, context=None):
        line = self.browse(cr, uid, line_id, context=context)
        move_data = self._prepare_produce_move(cr, uid, line,
                                               product_qty,
                                               context=context)
        move_id = False
        if move_data:
            move_id = self._create_stock_move(cr, uid, move_data,
                                              context=context)
            self._complete_stock_move(cr, uid, move_id, context=context)
        return move_id
