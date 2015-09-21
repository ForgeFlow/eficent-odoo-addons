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


class MrpBom(orm.Model):
    
    _inherit = 'mrp.bom'

    def write(self, cr, uid, ids, vals, context=None):
        res = super(MrpBom, self).write(cr, uid, ids, vals, context=context)
        if (
            'product_id' in vals or
            'product_qty' in vals or
            'product_uom' in vals or
            'bom_lines' in vals or
            'bom_id' in vals
        ):
            analytic_bom_obj = self.pool['analytic.bom']
            parent_boms = {}
            for bom in self.browse(cr, uid, ids, context=context):
                # Look for the parent BOMs
                parent_bom_id = False
                if bom.bom_id:
                    parent_bom_id = bom.bom_id
                else:
                    parent_boms[bom.id] = False
                while parent_bom_id:
                    if parent_bom_id.bom_id:
                        parent_bom_id = bom.bom_id
                    else:
                        parent_boms[parent_bom_id.id] = False
                    parent_bom_id = parent_bom_id.bom_id or False
            parent_bom_ids = parent_boms.keys()
            # Search for Analytic BOM lines containing the BOMs found
            for bom_id in parent_bom_ids:
                analytic_bom_ids = analytic_bom_obj.search(
                    cr, uid, [('bom_id', '=', bom_id),
                              ('state', '=', 'draft')], context=context)
                analytic_bom_obj.bom_explode_to_resource_plan(cr, uid,
                                                              analytic_bom_ids,
                                                              context=context)
        return res
