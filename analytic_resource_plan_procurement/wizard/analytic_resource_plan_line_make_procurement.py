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


class analytic_resouce_plan_line_make_procurement(orm.TransientModel):
    _name = "analytic.resource.plan.line.make.procurement"
    _description = "Resource plan make procurement"

    _columns = {
        'direct_ship': fields.boolean('Direct shipment',
                                      help='Deliver directly to the shipping '
                                      'address indicated in the Project or '
                                      'Analytic Account.')
    }

    _defaults = {
        'direct_ship': False,
    }

    def make_procurement(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = []
        make_procurement = self.browse(cr, uid, ids[0], context=context)
        record_ids = context and context.get('active_ids', False)
        if record_ids:            
            line_plan_obj = self.pool.get('analytic.resource.plan.line')
            procurement_obj = self.pool.get('procurement.order')
            company_id = False
            for line in line_plan_obj.browse(cr, uid, record_ids,
                                             context=context):
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

                if line.procurement_id:
                    raise orm.except_orm(
                        _('Could not create procurement !'),
                        _('A procurement order already exists '
                          'for one of the records selected.'))

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
                              ('procure_method', '=', 'make_to_order'),
                              ('analytic_account_id', '=',
                               line.account_id.id),
                              ('dest_address_id', '=', dest_address_id)],
                    context=context)
                if procurement_ids:
                    procurement_id = procurement_ids[0]
                    procurement = procurement_obj.browse(
                        cr, uid, procurement_id, context=context)
                    new_qty = procurement.product_qty + line.unit_amount
                    procurement_obj.write(cr, uid, [procurement.id],
                                          {'product_qty': new_qty},
                                          context=context)
                else:
                    procurement_id = procurement_obj.create(
                        cr, uid, line_plan_obj.prepare_procurement(
                            cr, uid, line,
                            direct_ship=make_procurement.direct_ship,
                            move_id=False, context=context))

                    wf_service = netsvc.LocalService("workflow")
                    wf_service.trg_validate(uid, 'procurement.order',
                                            procurement_id, 'button_confirm',
                                            cr)

                line_plan_obj.write(cr, uid, [line.id],
                                    {'procurement_id': procurement_id},
                                    context=context)
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