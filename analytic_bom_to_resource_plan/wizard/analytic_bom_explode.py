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
from openerp.tools.translate import _
from openerp.osv import fields, orm
import openerp.addons.decimal_precision as dp
import time


class AnalyticAssemblyToResourcePlan(orm.TransientModel):
    _name = "analytic.bom.to.resource.plan"
    _description = "Explode BOM to Resource Plan"

    def make_bom_explode(self, cr, uid, ids, context=None):
        """
             To create or update resource plan lines based on the bill of
             materials indicated in the analytic assembly.

             @param self: The object pointer.
             @param cr: A database cursor
             @param uid: ID of the user currently logged in
             @param ids: the ID or list of IDs
             @param context: A standard dictionary

             @return: A dictionary which of fields with values.

        """

        if context is None:
            context = {}
        res = []
        make_bom_explode = self.browse(cr, uid, ids[0], context=context)
        record_ids = context and context.get('active_ids', False)
        analytic_bom_obj = self.pool['analytic.bom']
        if record_ids:
            res = analytic_bom_obj.bom_explode_to_resource_plan(cr, uid,
                                                                record_ids,
                                                                context=context)

        return {
            'domain': "[('id','in', ["+','.join(map(str, res))+"])]",
            'name': _('New Resource Plan Lines'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'analytic.resource.plan.line',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }
