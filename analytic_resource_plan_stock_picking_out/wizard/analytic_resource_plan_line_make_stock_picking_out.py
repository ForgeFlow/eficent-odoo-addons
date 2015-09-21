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
import time
from openerp import netsvc
import openerp.addons.decimal_precision as dp


class AnalyticResourcePlanLineStockPickingOut(orm.TransientModel):
    _name = "analytic.resource.plan.line.stock.picking.out"
    _description = "Resource plan make delivery order"

    _columns = {
        'move_type': fields.selection([('direct', 'Partial'),
                                       ('one', 'All at once')],
                                      'Delivery Method', required=True,
                                      help="It specifies goods to be "
                                           "delivered partially or all "
                                           "at once"),
        'date': fields.datetime('Picking date',
                                help="Picking date",
                                required=True),
        'date_expected': fields.datetime('Scheduled Date',
                                         required=True,
                                         select=True,
                                         help="Scheduled date for the "
                                              "processing of the move."),
        'procure_method': fields.selection(
            [('make_to_stock', 'Make to Stock'),
             ('make_to_order', 'Make to Order')], 'Procurement Method',
            required=True,
            help="""If you specify 'Make to Order', the application will
            attempt to deliver from stock.
            \nIf you specify 'Make to Order', the application will raise
            a procurement order."""),
        'item_ids': fields.one2many(
            'analytic.resource.plan.line.stock.picking.out.item',
            'picking_out_wiz_id', 'Items'),
    }

    _defaults = {
        'move_type': 'direct',
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }

    def _prepare_item(self, cr, uid, line, context=None):
        return [{
            'product_id': line.product_id.id,
            'product_qty': line.unit_amount,
            'product_uom_id': line.product_uom_id.id,
            'line_id': line.id,
        }]

    def default_get(self, cr, uid, fields, context=None):
        res = super(AnalyticResourcePlanLineStockPickingOut, self).default_get(
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

    def _prepare_order_move(self, cr, uid, item, picking_id, date,
                            date_expected, context=None):
        line = item.line_id
        location_id = line.account_id.location_id \
            and line.account_id.location_id.id or False

        output_id = line.account_id.warehouse_id \
            and line.account_id.warehouse_id.lot_output_id\
            and line.account_id.warehouse_id.lot_output_id.id or False

        partner_id = line.account_id.dest_address_id \
            and line.account_id.dest_address_id.id or False,

        product_uom_id = line.product_uom_id \
            and line.product_uom_id.id or False

        return {
            'name': line.name,
            'picking_id': picking_id,
            'product_id': line.product_id.id,
            'date': date,
            'date_expected': date_expected,
            'product_qty': item.product_qty,
            'product_uom': product_uom_id,
            'product_uos_qty': line.unit_amount,
            'product_uos': product_uom_id,
            'partner_id': partner_id,
            'location_id': location_id,
            'location_dest_id': output_id,
            'analytic_account_id': line.account_id.id,
            'tracking_id': False,
            'state': 'draft',
            'company_id': line.account_id.company_id.id,
            'price_unit': 0.0
        }

    def _prepare_order_picking(self, cr, uid, line, date, move_type,
                               context=None):
        pick_name = self.pool.get('ir.sequence').get(cr, uid,
                                                     'stock.picking.out')
        return {
            'name': pick_name,
            'origin': line.account_id.name,
            'date': date,
            'type': 'out',
            'state': 'draft',
            'move_type': move_type,
            'partner_id': line.account_id.dest_address_id and
            line.account_id.dest_address_id.id or False,
            'invoice_state': 'none',
            'company_id': line.account_id.company_id.id,
        }

    def make_stock_picking_out(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = []
        make_picking = self.browse(cr, uid, ids[0], context=context)
        line_plan_obj = self.pool.get('analytic.resource.plan.line')
        picking_obj = self.pool.get('stock.picking.out')
        procurement_obj = self.pool.get('procurement.order')
        move_obj = self.pool.get('stock.move')
        wf_service = netsvc.LocalService("workflow")
        company_id = False
        dest_address_id = False
        picking_id = False
        proc_ids = []

        for item in make_picking.item_ids:
            line = item.line_id
            line_dest_address_id = line.account_id.dest_address_id \
                and line.account_id.dest_address_id.id or False
            if not line_dest_address_id:
                raise orm.except_orm(
                    _('Could not create Delivery Order !'),
                    _('You have to select lines '
                      'with a delivery address defined in the '
                      'Project / Analytic Account.'))

            if dest_address_id is not False \
                    and line_dest_address_id != dest_address_id:
                raise orm.except_orm(
                    _('Could not create Delivery Order !'),
                    _('You have to select lines '
                      'with the same delivery address.'))
            else:
                dest_address_id = line_dest_address_id

            if make_picking.date_expected < line.account_id.date_start:
                raise orm.except_orm(
                    _('Could not create Delivery Order !'),
                    _('The expected date must be after the '
                      'Project start date.'))

            if line.state != 'confirm':
                raise orm.except_orm(
                    _('Could not create Delivery Order !'),
                    _('All resource plan lines must be  '
                      'confirmed.'))

            if line.product_id \
                    and line.product_id.type not in ('product', 'consu'):
                raise orm.except_orm(
                    _('Could not create Delivery Order !'),
                    _('You have to select stockable or '
                      'consumable items.'))

            line_company_id = line.account_id.company_id \
                and line.account_id.company_id.id or False
            if company_id is not False \
                    and line_company_id != company_id:
                raise orm.except_orm(
                    _('Could not create Delivery Order !'),
                    _('You have to select lines '
                      'from the same company.'))
            else:
                company_id = line_company_id

            if picking_id is False:
                picking_id = picking_obj.create(
                    cr, uid, self._prepare_order_picking(
                        cr, uid, line, make_picking.date,
                        make_picking.move_type, context=context))
            move_data = self._prepare_order_move(
                    cr, uid, item, picking_id, make_picking.date,
                    make_picking.date_expected, context=context)
            move_id = move_obj.create(
                cr, uid, move_data, context=context)
            procurement_id = procurement_obj.create(
                cr, uid, line_plan_obj._prepare_procurement(
                    cr, uid, line, item.product_qty,
                    direct_ship=False, move_id=move_id,
                    context=context))
            proc_ids.append(procurement_id)
        if picking_id:
            res.append(picking_id)
            wf_service.trg_validate(uid, 'stock.picking', picking_id,
                                    'button_confirm', cr)
            # Check the availability
            picking_obj.action_assign(cr, uid, [picking_id])
        for proc_id in proc_ids:
            wf_service.trg_validate(uid, 'procurement.order', proc_id,
                                    'button_confirm', cr)

        return {
            'domain': "[('id','in', ["+','.join(map(str, res))+"])]",
            'name': _('Delivery Orders'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking.out',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }


class AnalyticResourcePlanLineStockPickingOutItem(orm.TransientModel):
    _name = "analytic.resource.plan.line.stock.picking.out.item"
    _description = "Resource plan make delivery order item"

    _columns = {
        'picking_out_wiz_id': fields.many2one(
            'analytic.resource.plan.line.stock.picking.out',
            'Picking Wizard', required=True, ondelete='cascade',
            readonly=True),
        'line_id': fields.many2one('analytic.resource.plan.line',
                                   'Resource Plan Line',
                                   required=True,
                                   readonly=True),
        'product_qty': fields.float(string='Quantity to deliver',
                                    digits_compute=dp.get_precision(
                                        'Product UoS')),
        'product_uom_id': fields.related('line_id',
                                         'product_uom_id', type='many2one',
                                         relation='product.uom',
                                         string='UoM',
                                         readonly=True)
    }
