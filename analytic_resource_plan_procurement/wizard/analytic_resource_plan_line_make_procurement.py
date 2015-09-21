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


class AnalyticResourcePlanLineMakeProcurement(orm.TransientModel):
    _name = "analytic.resource.plan.line.make.procurement"
    _description = "Resource plan make procurement"

    _columns = {
        'direct_ship': fields.boolean('Direct shipment',
                                      help='Deliver directly to the shipping '
                                      'address indicated in the Project or '
                                      'Analytic Account.'),
        'procure_method': fields.selection(
            [('make_to_stock', 'Make to Stock'),
             ('make_to_order', 'Make to Order')],
            'Procurement Method',
            readonly=True),
        'item_ids': fields.one2many(
            'analytic.resource.plan.line.make.procurement.item',
            'wiz_id', 'Items'),
    }

    _defaults = {
        'direct_ship': False,
        'procure_method': 'make_to_order',
    }

    def _prepare_item(self, cr, uid, line, context=None):
        return [{
            'product_id': line.product_id.id,
            'product_qty': line.unit_amount,
            'product_uom_id': line.product_uom_id.id,
            'line_id': line.id,
        }]

    def default_get(self, cr, uid, fields, context=None):
        res = super(AnalyticResourcePlanLineMakeProcurement, self).default_get(
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

    def make_procurement(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = []
        make_procurement = self.browse(cr, uid, ids[0], context=context)
        line_plan_obj = self.pool.get('analytic.resource.plan.line')
        procurement_obj = self.pool.get('procurement.order')
        company_id = False
        for item in make_procurement.item_ids:
            line = item.line_id
            if line.product_id.type == 'service'\
                    and line.product_id.supply_method == 'produce':
                raise orm.except_orm(
                    _('Could not create procurement !'),
                    _("""An item exists with a product with
                    Product Type 'Service' and
                    Supply Method 'Manufacture'."""))

            if make_procurement.direct_ship \
                    and not line.account_id.dest_address_id:
                raise orm.except_orm(
                    _('Could not create procurement !'),
                    _('A delivery address must be indicated in '
                      'the Project.'))

            if line.state != 'confirm':
                raise orm.except_orm(
                    _('Could not create procurement !'),
                    _('All resource plan lines must be  '
                      'confirmed.'))

            if item.product_qty < 0.0:
                raise orm.except_orm(
                    _('Could not create procurement !'),
                    _('Enter a positive quantity.'))

            line_company_id = line.account_id.company_id \
                and line.account_id.company_id.id or False
            if company_id is not False \
                    and line_company_id != company_id:
                raise orm.except_orm(
                    _('Could not create procurement !'),
                    _('You have to select lines '
                      'from the same company.'))
            else:
                company_id = line_company_id

            if not line.account_id.date_start:
                raise orm.except_orm(
                    _('Could not create procurement !'),
                    _('The project/analytic account has '
                      'no start date. This date is used '
                      'as the scheduled date for the '
                      'procurement.'))
            # Search for an existing procurement order that is draft or
            # confirmed, for that same product, UoM, location, delivery
            # address, procurement method, product, BOM. If found,
            # then add the extra quantity to it.
            dest_address_id = line.account_id.dest_address_id \
                and line.account_id.dest_address_id.id or False
            location_id = line.account_id.location_id \
                and line.account_id.location_id.id or False

            procurement_ids = procurement_obj.search(
                cr, uid, [('state', 'in', ['draft', 'confirmed']),
                          ('product_id', '=', line.product_id.id),
                          ('product_uom', '=', line.product_uom_id.id),
                          ('location_id', '=', location_id),
                          ('procure_method', '=',
                           make_procurement.procure_method),
                          ('analytic_account_id', '=',
                           line.account_id.id),
                          ('dest_address_id', '=', dest_address_id)],
                context=context)
            if procurement_ids:
                procurement_id = procurement_ids[0]
                procurement = procurement_obj.browse(
                    cr, uid, procurement_id, context=context)
                new_qty = procurement.product_qty + item.product_qty
                procurement_obj.write(
                    cr, uid, [procurement.id],
                    {'product_qty': new_qty,
                     'procurement_orders': [(4, [line.id])]},
                    context=context)
            else:
                procurement_id = procurement_obj.create(
                    cr, uid, line_plan_obj._prepare_procurement(
                        cr, uid, line, item.product_qty,
                        procure_method=make_procurement.procure_method,
                        direct_ship=make_procurement.direct_ship,
                        move_id=False, context=context))

                wf_service = netsvc.LocalService("workflow")
                wf_service.trg_validate(uid, 'procurement.order',
                                        procurement_id, 'button_confirm',
                                        cr)
            res.append(procurement_id)

        return {
            'domain': "[('id','in', ["+','.join(map(str, res))+"])]",
            'name': _('Procurement orders'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'procurement.order',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }


class AnalyticResourcePlanLineMakeProcurementItem(orm.TransientModel):
    _name = "analytic.resource.plan.line.make.procurement.item"
    _description = "Resource plan make procurement item"

    _columns = {
        'wiz_id': fields.many2one(
            'analytic.resource.plan.line.make.procurement',
            'Wizard', required=True, ondelete='cascade',
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
