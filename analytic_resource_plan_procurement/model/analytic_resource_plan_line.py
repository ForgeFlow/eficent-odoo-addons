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
from openerp.tools.translate import _

PROCUREMENT_STATES = [
    ('draft', 'Draft'),
    ('cancel', 'Cancelled'),
    ('confirmed', 'Confirmed'),
    ('exception', 'Exception'),
    ('running', 'Running'),
    ('ready', 'Ready'),
    ('done', 'Done'),
    ('waiting', 'Waiting')
]


class analytic_resource_plan_line(orm.Model):
    
    _inherit = 'analytic.resource.plan.line'

    _columns = {
        'procurement_id': fields.many2one('procurement.order',
                                          'Procurement Order',
                                          readonly=True),
        'procurement_state': fields.related('procurement_id', 'state',
                                            type="selection",
                                            selection=PROCUREMENT_STATES,
                                            relation="procurement.order",
                                            string="Procurement State",
                                            readonly=True),
    }

    def prepare_procurement(self, cr, uid, line, direct_ship=False,
                            move_id=False, context=None):
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
            'product_qty': line.unit_amount,
            'product_uom': product_uom_id,
            'location_id': location_id,
            'procure_method': 'make_to_order',
            'company_id': line.account_id.company_id.id,
            'analytic_account_id': line.account_id.id,
            'dest_address_id': dest_address_id,
            'move_id': move_id,
        }

    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}
        default['procurement_id'] = False
        res = super(analytic_resource_plan_line, self).copy(
            cr, uid, id, default, context)
        return res

    def action_button_draft(self, cr, uid, ids, context=None):
        for line in self.browse(cr, uid, ids, context=context):
            if line.procurement_id:
                raise orm.except_orm(
                    _('Invalid action.'),
                    _('You cannot reset a confirmed resource  '
                      'plan line that has a procurement order.'
                      'First cancel the order.'))
        return super(analytic_resource_plan_line, self).\
            action_button_draft(cr, uid, ids, context=context)
