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


class AnalyticBom(orm.Model):
    
    _inherit = 'analytic.bom'

    _columns = {
        'resource_plan_line_ids': fields.one2many(
            'analytic.resource.plan.line',
            'analytic_bom_id',
            'Resource Plan Lines'),
    }

    def bom_explode_to_resource_plan(self, cr, uid, ids, context=None):
        bom_obj = self.pool['mrp.bom']
        uom_obj = self.pool['product.uom']
        plan_line_obj = self.pool['analytic.resource.plan.line']
        res = []
        for bom in self.browse(cr, uid, ids, context=context):
                if bom.state != 'draft':
                    continue
                factor = uom_obj._compute_qty(
                    cr, uid, bom.product_uom_id.id,
                    bom.product_qty,
                    bom.bom_id.product_uom.id)
                bom_res = bom_obj._bom_explode(
                    cr, uid, bom.bom_id,
                    factor / bom.bom_id.product_qty,
                    routing_id=False)
                components = bom_res[0]  # product_lines
                for line in components:
                    plan_line_ids = plan_line_obj.search(
                        cr, uid, [('analytic_bom_id', '=',
                                   bom.id),
                                  ('product_id', '=',
                                   line['product_id']),
                                  ('product_uom_id', '=',
                                   line['product_uom']),
                                  ('account_id', '=',
                                   bom.account_id.id),
                                  ('state', '=', 'draft')],
                        context=context)
                    plan_line_obj.unlink(cr, uid, plan_line_ids,
                                         context=context)
                    plan_line_ids = plan_line_obj.search(
                        cr, uid, [('analytic_bom_id', '=',
                                   bom.id),
                                  ('product_id', '=',
                                   line['product_id']),
                                  ('product_uom_id', '=',
                                   line['product_uom']),
                                  ('account_id', '=',
                                   bom.account_id.id),
                                  ('state', '=', 'confirm')],
                        context=context)
                    total_qty = 0.0
                    for plan_line in plan_line_obj.browse(cr, uid,
                                                          plan_line_ids,
                                                          context=context):
                        total_qty += plan_line.unit_amount

                    if line['product_qty'] > total_qty:
                        resource_line = {
                            'account_id': bom.account_id.id,
                            'name': line['name'],
                            'date': bom.date_planned,
                            'state': 'draft',
                            'product_id': line['product_id'],
                            'product_uom_id': line['product_uom'],
                            'unit_amount': line['product_qty'] - total_qty,
                            'analytic_bom_id': bom.id,
                        }
                        plan_id = plan_line_obj.create(cr, uid, resource_line,
                                                       context=context)
                        res.append(plan_id)
        return res
