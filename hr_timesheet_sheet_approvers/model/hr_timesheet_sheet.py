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
from openerp.tools.translate import _
from openerp import netsvc


class hr_timesheet_sheet(osv.osv):
    _inherit = "hr_timesheet_sheet.sheet"

    def _get_approver_user_ids(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for timesheet in self.browse(cursor, user, ids, context=context):
            res[timesheet.id] = []
            if timesheet.employee_id \
                    and timesheet.employee_id.parent_id \
                    and timesheet.employee_id.parent_id.user_id:
                res[timesheet.id].append(
                    timesheet.employee_id.parent_id.user_id.id)
            if timesheet.department_id \
                    and timesheet.department_id.manager_id \
                    and timesheet.department_id.manager_id.user_id:
                res[timesheet.id].append(
                    timesheet.department_id.manager_id.user_id.id)
        return res

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
        'approver_user_ids': fields.function(_get_approver_user_ids,
                                             type='many2many',
                                             string='Timesheet Approver users',
                                             method=True,
                                             readonly=True),
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

    def action_set_to_draft(self, cr, uid, ids, *args):
        for timesheet in self.browse(cr, uid, ids):
            if uid not in timesheet.approver_user_ids:
                raise osv.except_osv(_('Invalid Action!'),
                                     _('You are not authorised to approve '
                                       'this Timesheet.'))
        return super(hr_timesheet_sheet, self).action_set_to_draft(
            cr, uid, ids, *args)

    def action_done(self, cr, uid, ids, *args):
        for timesheet in self.browse(cr, uid, ids):
            if uid not in timesheet.approver_user_ids:
                raise osv.except_osv(_('Invalid Action!'),
                                     _('You are not authorised to approve '
                                       'this Timesheet.'))
        self.write(cr, uid, ids, {'state': 'done'})
        wf_service = netsvc.LocalService('workflow')
        for id in ids:
            wf_service.trg_create(uid, self._name, id, cr)
        return True

    def action_cancel(self, cr, uid, ids, *args):
        for timesheet in self.browse(cr, uid, ids):
            if uid not in timesheet.approver_user_ids:
                raise osv.except_osv(_('Invalid Action!'),
                                     _('You are not authorised to approve '
                                       'this Timesheet.'))
        self.write(cr, uid, ids, {'state': 'cancel'})
        wf_service = netsvc.LocalService('workflow')
        for id in ids:
            wf_service.trg_create(uid, self._name, id, cr)
        return True