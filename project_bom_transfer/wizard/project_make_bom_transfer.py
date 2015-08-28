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
from openerp.tools.translate import _
from openerp.osv import fields, orm
import openerp.addons.decimal_precision as dp
import time


class ProjectMakeBomTransfer(orm.TransientModel):
    _name = "project.make.bom.transfer"
    _description = "Project Make BOM Transfer"

    _columns = {
        'product_id': fields.many2one('product.product', 'Product',
                                      required=True),
        'bom_id': fields.many2one('mrp.bom', 'Bill of Materials',
                                  domain=[('bom_id', '=', False)],
                                  required=True),
        'product_qty': fields.float(
            'Product Quantity',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            required=True),
        'product_uom_id': fields.many2one('product.uom',
                                          'Product Unit of Measure',
                                          required=True),
        'date_planned': fields.datetime('Scheduled Date', required=True),
    }

    _defaults = {
        'product_qty': lambda *a: 1.0,
        'date_planned': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }

    def product_id_change(self, cr, uid, ids, product_id, context=None):
        """ Finds UoM of changed product.
        @param product_id: Id of changed product.
        @return: Dictionary of values.
        """
        if not product_id:
            return {'value': {
                'product_uom': False,
                'bom_id': False,
            }}
        bom_obj = self.pool.get('mrp.bom')
        product = self.pool.get('product.product').browse(cr, uid, product_id,
                                                          context=context)
        bom_id = bom_obj._bom_find(cr, uid, product.id, product.uom_id and
                                   product.uom_id.id, [])
        product_uom_id = product.uom_id and product.uom_id.id or False
        result = {
            'product_uom_id': product_uom_id,
            'bom_id': bom_id
        }
        return {'value': result}

    def make_bom_transfer(self, cr, uid, ids, context=None):
        """
             To create or update resource plan lines based on the bill of
             materials indicated on a project.

             @param self: The object pointer.
             @param cr: A database cursor
             @param uid: ID of the user currently logged in
             @param ids: the ID or list of IDs
             @param context: A standard dictionary

             @return: A dictionary which of fields with values.

        """

        if context is None:
            context = {}
        res = []
        make_bom_transfer = self.browse(cr, uid, ids[0], context=context)
        record_ids = context and context.get('active_ids', False)
        bom_obj = self.pool['mrp.bom']
        uom_obj = self.pool['product.uom']
        project_obj = self.pool['project.project']
        plan_line_obj = self.pool['analytic.resource.plan.line']
        if record_ids:
            for project in project_obj.browse(cr, uid, record_ids,
                                              context=context):
                factor = uom_obj._compute_qty(
                    cr, uid, make_bom_transfer.product_uom_id.id,
                    make_bom_transfer.product_qty,
                    make_bom_transfer.bom_id.product_uom.id)
                bom_res = bom_obj._bom_explode(
                    cr, uid, make_bom_transfer.bom_id,
                    factor / make_bom_transfer.bom_id.product_qty,
                    routing_id=False)
                components = bom_res[0]  # product_lines
                for line in components:
                    plan_line_ids = plan_line_obj.search(
                        cr, uid, [('bom_id', '=',
                                   make_bom_transfer.bom_id.id),
                                  ('product_id', '=',
                                   line['product_id']),
                                  ('product_uom_id', '=',
                                   line['product_uom']),
                                  ('account_id', '=',
                                   project.analytic_account_id.id)],
                        context=context)
                    total_qty = 0.0
                    for plan_line in plan_line_obj.browse(cr, uid,
                                                          plan_line_ids,
                                                          context=context):
                        total_qty += plan_line.unit_amount

                    if line['product_qty'] > total_qty:
                        resource_line = {
                            'account_id': project.analytic_account_id.id,
                            'name': line['name'],
                            'date': make_bom_transfer.date_planned,
                            'state': 'draft',
                            'product_id': line['product_id'],
                            'product_uom_id': line['product_uom'],
                            'unit_amount': line['product_qty'] - total_qty,
                            'bom_id': make_bom_transfer.bom_id.id,
                        }
                        plan_id = plan_line_obj.create(cr, uid, resource_line,
                                                       context=context)
                        res.append(plan_id)

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
