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

from openerp.osv import fields, osv


class hr_timesheet_sheet(osv.osv):
    _inherit = "hr_timesheet_sheet.sheet"

    _columns = {
        'employee_manager_id': fields.related('employee_id', 'parent_id',
                                              type="many2one",
                                              relation="hr.employee",
                                              store=False,
                                              string="Employee's Manager",
                                              required=False, readonly=True),
        'department_manager_id': fields.related('department_id', 'manager_id',
                                                type="many2one",
                                                relation="hr.employee",
                                                store=False,
                                                string="Department's Manager",
                                                required=False, readonly=True),
    }

    def button_confirm(self, cr, uid, ids, context=None):
        for sheet in self.browse(cr, uid, ids, context=context):
            if sheet.department_id and sheet.department_id.manager_id \
                    and sheet.department_id.manager_id.user_id:
                    self.message_subscribe_users(
                        cr, uid, [sheet.id],
                        user_ids=[sheet.department_id.manager_id.user_id.id],
                        context=context)
        return super(hr_timesheet_sheet, self).button_confirm(cr, uid, ids,
                                                              context=context)
