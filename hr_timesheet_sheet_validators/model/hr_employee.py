# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import orm, fields
from openerp.tools.translate import _
from openerp import netsvc


class hr_employee(orm.Model):
    _inherit = "hr.employee"

    def get_validator_user_ids(self, cr, uid, ids, context=None):
        res = {}
        users = {}
        for employee in self.browse(cr, uid, ids):
            res[employee.id] = []
            users[employee.id] = []
            if (
                employee
                and employee.parent_id
                and employee.parent_id.user_id
            ):
                users[employee.id].append(
                    employee.parent_id.user_id.id)
            if (
                employee.department_id
                and employee.department_id.manager_id
                and employee.department_id.manager_id.user_id
                and employee.department_id.manager_id.user_id.id != uid
            ):
                users[employee.id].append(
                    employee.department_id.manager_id.user_id.id)
            elif (
                employee.department_id
                and employee.department_id.parent_id
                and employee.department_id.parent_id.manager_id
                and employee.department_id.parent_id.manager_id.user_id
                and employee.department_id.parent_id.
                    manager_id.user_id.id != uid
            ):
                users[employee.id].append(
                    employee.department_id.manager_id.user_id.id)

            [res[employee.id].append(item) for item in users[employee.id]
             if item not in res[employee.id]]
        return res