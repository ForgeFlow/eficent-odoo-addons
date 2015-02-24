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


class procurement_order(orm.Model):
    
    _inherit = 'procurement.order'

    def action_cancel(self, cr, uid, ids):
        if not len(ids):
            return True
        res_plan_line_obj = self.pool.get('analytic.resource.plan.line')
        for proc in self.browse(cr, uid, ids):
            line_ids = res_plan_line_obj.search(
                cr, uid, [('procurement_id', '=', proc.id)], context=None)
            res_plan_line_obj.write(cr, uid, line_ids,
                                    {'procurement_id': False}, context=None)
        return super(procurement_order, self).action_cancel(cr, uid, ids)