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


class AnalyticRPLDoStockRelease(orm.TransientModel):
    _name = "analytic.rpl.do.stock.release"
    _description = "Resource plan release stock quantity"

    def do_stock_release(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        resource_plan_obj = self.pool['analytic.resource.plan.line']
        resource_plan_line_ids = context.get('active_ids', [])
        active_model = context.get('active_model')

        if not resource_plan_line_ids:
            return True
        assert active_model == 'analytic.resource.plan.line', \
            'Bad context propagation'
        resource_plan_obj.release_stock_reservation(cr, uid,
                                                    resource_plan_line_ids,
                                                    context=context)
        return True
