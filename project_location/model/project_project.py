# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#               <contact@eficent.com>
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


class project(orm.Model):
    _inherit = "project.project"

    def get_parent_stock_data(self, cr, uid, context=None):
        if context is None:
            context = {}
        res = {}
        project_obj = self.pool.get('project.project')
        if 'default_parent_id' in context and context['default_parent_id']:
            for project_id in project_obj.search(
                    cr, uid, [('analytic_account_id', '=',
                               context['default_parent_id'])]):
                project = project_obj.browse(cr, uid, project_id, context=context)
                res['location_id'] = project.location_id and \
                    project.location_id.id or False
                res['dest_address_id'] = project.dest_address_id and \
                    project.dest_address_id.id or False
        return res

    def _get_parent_location(self, cr, uid, context=None):
        if context is None:
            context = {}
        res = self.pool.get('project.project').get_parent_stock_data(
            cr, uid, context=context)
        if 'location_id' in res:
            return res['location_id']
        else:
            return False

    def _get_parent_dest_address(self, cr, uid, context=None):
        if context is None:
            context = {}
        res = self.pool.get('project.project').get_parent_stock_data(
            cr, uid, context=context)
        if 'dest_address_id' in res:
            return res['dest_address_id']
        else:
            return False

    _defaults = {
        'location_id': _get_parent_location,
        'dest_address_id': _get_parent_dest_address,
    }
