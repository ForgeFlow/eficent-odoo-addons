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


class stock_move(orm.Model):

    _inherit = "stock.move"

    def action_cancel(self, cr, uid, ids, context=None):
        if not len(ids):
            return True
        if context is None:
            context = {}
        res_plan_line_obj = self.pool.get('analytic.resource.plan.line')
        for move in self.browse(cr, uid, ids):
            line_ids = res_plan_line_obj.search(
                cr, uid, [('picking_out_move_id', '=', move.id)],
                context=None)
            res_plan_line_obj.write(cr, uid, line_ids,
                                    {'picking_out_move_id': False},
                                    context=None)
        return super(stock_move, self).action_cancel(cr, uid, ids,
                                                     context=context)