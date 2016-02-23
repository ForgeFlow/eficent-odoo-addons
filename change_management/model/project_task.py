# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Enterprise Management Solution
#
#    Copyright (C) 2015 Matmoz d.o.o. (<http://www.matmoz.si>).
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
from openerp.osv import fields, osv


class project_task(osv.osv):
    _name = 'project.task'
    _inherit = 'project.task'

    _columns = {
        'change_id': fields.many2one('change.management.change',
                                     'Action on Change', readonly=True,
        help="Task is an action on a change identified by this label."
    ),
    }


class project_project(osv.osv):
    _name = 'project.project'
    _inherit = 'project.project'

    _columns = {
    'change_ids': fields.one2many('change.management.change', 'project_id',
                                  'Project changes')
    }
