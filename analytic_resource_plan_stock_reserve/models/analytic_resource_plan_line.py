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

    def _get_reserved_qty(self, cr, uid, ids, field_names, arg, context=None):
        if not context:
            context = {}
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = 0.0
            for sr in line.stock_reservation_ids:
                if sr.state == 'assigned':
                    res[line.id] += sr.product_qty
        return res

    _columns = {
        'stock_reservation_ids': fields.one2many(
            'stock.reservation',
            'analytic_resource_plan_line_id',
            readonly=True),
        'reserved_qty': fields.function(_get_reserved_qty, method=True,
                                        type='float',
                                        readonly=True,
                                        string='Reserved quantity'),
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}
        default['stock_reservation_ids'] = []
        return super(AnalyticResourcePlanLine, self).copy(cr, uid, id, default,
                                                          context)

    def action_button_draft(self, cr, uid, ids, context=None):
        self.release_stock_reservation(cr, uid, ids, context=context)
        return super(AnalyticResourcePlanLine, self).action_button_draft(
            cr, uid, ids, context=context)

    def _prepare_reservation(self, cr, uid, line, context=None):
            name = 'Reserve %s %s of %s for %s' % (line.unit_amount,
                                                   line.product_uom_id.name,
                                                   line.product_id.name,
                                                   line.account_id.name)
            if not line.account_id.location_id:
                raise orm.except_orm(
                    _('Error'),
                    _('The analytic account must contain a default Location.'))
            return {
                'product_id': line.product_id.id,
                'product_qty': line.unit_amount,
                'product_uom': line.product_uom_id.id,
                'name': name,
                'location_id': line.account_id.location_id.id,
                'analytic_account_id': line.account_id.id,
                'analytic_resource_plan_line_id': line.id
            }

    def _create_reservation(self, cr, uid, data, context=None):
        reservation_obj = self.pool['stock.reservation']
        return reservation_obj.create(cr, uid, data, context=context)

    def _confirm_reservation(self, cr, uid, reservation_id, context=None):
        reservation_obj = self.pool['stock.reservation']
        return reservation_obj.reserve(cr, uid, [reservation_id],
                                       context=context)

    def action_button_confirm(self, cr, uid, ids, context=None):
        self.reserve_stock(cr, uid, ids, context=context)
        return super(AnalyticResourcePlanLine, self).action_button_confirm(
            cr, uid, ids, context=context)

    def button_stock_reserve(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.reserve_stock(cr, uid, ids, context=context)
        return True

    def button_stock_release(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.release_stock_reservation(cr, uid, ids, context=context)
        return True

    def release_stock_reservation(self, cr, uid, ids, context=None):
        reservation_obj = self.pool['stock.reservation']
        for line in self.browse(cr, uid, ids, context=context):
            if line.reserved_qty > 0:
                sr_ids = [sr.id for sr in line.stock_reservation_ids]
                reservation_obj.release(cr, uid, sr_ids, context=context)
        return True

    def reserve_stock(self, cr, uid, ids, context=None):
        for line in self.browse(cr, uid, ids, context=context):
            if line.product_id.type in ('consu', 'product') and \
                    line.unit_amount > 0 and not line.reserved_qty:
                reservation_data = self._prepare_reservation(
                    cr, uid, line, context=context)
                reservation_id = self._create_reservation(cr, uid,
                                                          reservation_data,
                                                          context=context)
                self._confirm_reservation(cr, uid, reservation_id,
                                          context=context)
        return True
