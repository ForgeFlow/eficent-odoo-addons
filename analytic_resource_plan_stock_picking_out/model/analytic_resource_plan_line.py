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

STOCK_MOVE_STATES = [
    ('draft', 'New'),
    ('cancel', 'Cancelled'),
    ('waiting', 'Waiting Another Move'),
    ('confirmed', 'Waiting Availability'),
    ('assigned', 'Available'),
    ('done', 'Done')
]


class analytic_resource_plan_line(orm.Model):
    
    _inherit = 'analytic.resource.plan.line'

    _columns = {
        'picking_out_move_id': fields.many2one('stock.move',
                                               'Delivery Stock Move',
                                               readonly=True),
        'picking_out_move_state': fields.related('picking_out_move_id',
                                                 'state',
                                                 type="selection",
                                                 selection=STOCK_MOVE_STATES,
                                                 relation="stock.move",
                                                 string="Delivery Move State",
                                                 readonly=True),
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}
        default['picking_out_move_id'] = []
        res = super(analytic_resource_plan_line, self).copy(
            cr, uid, id, default, context)
        return res

    def action_button_draft(self, cr, uid, ids, context=None):
        for line in self.browse(cr, uid, ids, context=context):
            if line.picking_out_move_id:
                raise orm.except_orm(
                    _('Invalid action.'),
                    _('You cannot reset a confirmed resource  '
                      'plan line that has a procurement order.'
                      'First cancel the order.'))
        return super(analytic_resource_plan_line, self).\
            action_button_draft(cr, uid, ids, context=context)