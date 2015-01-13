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

    def _get_approver_user_ids(self, cr, uid, ids, *args):
        res = {}
        for timesheet in self.browse(cr, uid, ids):
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

    def _check_authorised_validator(self, cr, uid, ids, *args):
        model_data_obj = self.pool.get('ir.model.data')
        res_groups_obj = self.pool.get("res.groups")
        group_hr_manager_id = model_data_obj._get_id(
            cr, uid, 'base', 'group_hr_manager')
        group_hr_user_id = model_data_obj._get_id(
            cr, uid, 'base', 'group_hr_user')
        group_hr_user_ids = []
        group_hr_manager_ids = []
        if group_hr_manager_id:
                res_id = model_data_obj.read(cr, uid, [group_hr_manager_id],
                                             ['res_id'])[0]['res_id']
                group_hr_manager = res_groups_obj.browse(
                    cr, uid, res_id)
                group_hr_manager_ids = [user.id for user
                                  in group_hr_manager.users]
        if group_hr_user_id:
                res_id = model_data_obj.read(cr, uid, [group_hr_user_id],
                                             ['res_id'])[0]['res_id']
                group_hr_user = res_groups_obj.browse(
                    cr, uid, res_id)
                group_hr_user_ids = [user.id for user
                                  in group_hr_user.users]

        approver_ids = self._get_approver_user_ids(cr, uid, ids, *args)
        for timesheet in self.browse(cr, uid, ids):
            if uid not in approver_ids[timesheet.id] \
                    and uid not in group_hr_manager_ids \
                    and uid not in group_hr_user_ids:
                    raise osv.except_osv(_('Invalid Action!'),
                                         _('You are not authorised to approve '
                                           'or refuse this Timesheet.'))

    def action_set_to_draft(self, cr, uid, ids, *args):
        self._check_authorised_validator(cr, uid, ids, *args)
        return super(hr_timesheet_sheet, self).action_set_to_draft(
            cr, uid, ids, *args)

    def action_done(self, cr, uid, ids, *args):
        self._check_authorised_validator(cr, uid, ids, *args)
        wf_service = netsvc.LocalService('workflow')
        for id in ids:
            wf_service.trg_validate(uid, 'hr_timesheet_sheet.sheet',
                                    id, 'done', cr)
        return True

    def action_cancel(self, cr, uid, ids, *args):
        self._check_authorised_validator(cr, uid, ids, *args)
        wf_service = netsvc.LocalService('workflow')
        for id in ids:
            wf_service.trg_validate(uid, 'hr_timesheet_sheet.sheet',
                                    id, 'cancel', cr)
        return True