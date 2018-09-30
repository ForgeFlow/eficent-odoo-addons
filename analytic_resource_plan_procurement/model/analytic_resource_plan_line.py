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
from openerp.osv import fields, orm


class AnalyticResourcePlanLine(orm.Model):

    _inherit = 'analytic.resource.plan.line'

    _columns = {
        'procurement_orders': fields.many2many(
            'procurement.order',
            'procurement_order_analytic_resource_plan_line_line_rel',
            'analytic_resource_plan_line_id',
            'procurement_order_id',
            'Procurement Orders', readonly=True),
        'procurement_id': fields.many2one('procurement.order', required=False),
        'procurement_state': fields.boolean('Procurement state')
    }

    def _prepare_procurement(self, cr, uid, line, product_qty,
                             direct_ship=False,
                             procure_method='make_to_order', move_id=False,
                             context=None):
        location_id = line.account_id.location_id \
            and line.account_id.location_id.id or False
        if direct_ship:
            dest_address_id = line.account_id.dest_address_id \
                and line.account_id.dest_address_id.id or False
        else:
            dest_address_id = False

        product_uom_id = line.product_uom_id \
            and line.product_uom_id.id or False
        return {
            'name': line.name,
            'origin': line.account_id.complete_name,
            'date_planned': line.account_id.date_start or False,
            'product_id': line.product_id.id,
            'product_qty': product_qty,
            'product_uom': product_uom_id,
            'location_id': location_id,
            'procure_method': procure_method,
            'company_id': line.account_id.company_id.id,
            'analytic_account_id': line.account_id.id,
            'dest_address_id': dest_address_id,
            'move_id': move_id,
            'analytic_resource_plan_lines': [(4, [line.id])]
        }
