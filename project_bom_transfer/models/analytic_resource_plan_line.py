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


class AnalyticResourcePlanLine(orm.Model):
    
    _inherit = 'analytic.resource.plan.line'

    _columns = {
        'bom_id': fields.many2one('mrp.bom',
                                  'Bill of Materials',
                                  readonly=True),
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}
        default['bom_id'] = False
        res = super(AnalyticResourcePlanLine, self).copy(
            cr, uid, id, default, context)
        return res

    def action_button_cancel(self, cr, uid, ids, context=None):
        res = super(AnalyticResourcePlanLine, self). action_button_cancel(
            cr, uid, ids, context=context)
        self.write(cr, uid, ids, {'bom_id': False}, context=context)
        return res
