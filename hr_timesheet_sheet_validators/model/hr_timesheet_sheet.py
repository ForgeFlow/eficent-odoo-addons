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


class hr_timesheet_sheet(orm.Model):
    _inherit = "hr_timesheet_sheet.sheet"

    _columns = {
        'validator_user_ids': fields.many2many('res.users', string='Validators',
                                               required=False),
    }

    def _default_department(self, cr, uid, context=None):
        emp_obj = self.pool.get('hr.employee')
        emp_ids = emp_obj.search(cr, uid, [('user_id', '=', uid)],
                                 context=context)
        emps = emp_obj.browse(cr, uid, emp_ids, context=context)

        for emp in emps:
            return emp.department_id and emp.department_id.id or False
        return False

    _defaults = {
        'department_id': _default_department,
    }

    def create(self, cr, uid, vals, context=None):
        employee = vals.get('employee_id', False)
        if employee:
            validators = self.pool.get('hr.employee').get_validator_user_ids(
                cr, uid, [employee], context=context)
            vals['validator_user_ids'] = [(4, user_id) for user_id in validators[employee]]
        return super(hr_timesheet_sheet, self).create(
            cr, uid, vals, context=context)

    def _check_authorised_validator(self, cr, uid, ids, *args):
        for timesheet in self.browse(cr, uid, ids):
            validator_user_ids = []
            for validator_user_id in timesheet.validator_user_ids:
                validator_user_ids.append(validator_user_id.id)
            if uid not in validator_user_ids:
                raise orm.except_orm(_('Invalid Action!'),
                                     _('You are not authorised to approve'
                                       ' or refuse this Timesheet.'))

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
