# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _
from openerp import netsvc
from openerp.exceptions import UserError


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet_sheet.sheet"

    validator_user_ids = fields.Many2many(
        'res.users', string='Validators')

    @api.model
    def _default_department(self):
        employees = self.env['hr.employee'].search([
            ('user_id', '=', self.env.uid)])
        for emp in employees:
            return emp.department_id and emp.department_id.id or False
        return False

    _defaults = {
        'department_id': _default_department,
    }

    @api.multi
    def _get_validator_user_ids(self):
        """Return the list of user_ids that can validate a given timesheet."""
        self.ensure_one()
        for timesheet in self:
            users = []
            if (timesheet.employee_id and timesheet.employee_id.parent_id
                    and timesheet.employee_id.parent_id.user_id):
                users.append(
                    timesheet.employee_id.parent_id.user_id.id)
            if (timesheet.department_id and timesheet.department_id.manager_id
                    and timesheet.department_id.manager_id.user_id
                    and timesheet.department_id.manager_id.user_id.id !=
                    self.env.uid):
                users.append(
                    timesheet.department_id.manager_id.user_id.id)
            elif (timesheet.department_id and timesheet.department_id.parent_id
                    and timesheet.department_id.parent_id.manager_id
                    and timesheet.department_id.parent_id.manager_id.user_id
                    and timesheet.department_id.parent_id.manager_id.
                        user_id.id != self.env.uid):
                users.append(
                    timesheet.department_id.manager_id.user_id.id)
            return list(set(users)) if users else []

    @api.multi
    def button_confirm(self):
        for sheet in self:
            validators = sheet._get_validator_user_ids()
            sheet.write({'validator_user_ids': [(6, 0, validators)]})
        return super(HrTimesheetSheet, self).button_confirm()

    @api.multi
    def _check_authorised_validator(self):
        group_hr_manager = self.env.ref('base.group_hr_manager')
        group_hr_user = self.env.ref('base.group_hr_user')
        for timesheet in self:
            if group_hr_manager and self.env.uid in group_hr_manager.users.ids:
                continue

            if group_hr_user and self.env.uid in group_hr_user.users.ids:
                continue

            # TODO: check this:
            # TODO: this is not raising, why?:
            if self.env.uid not in timesheet.validator_user_ids.ids:
                raise UserError(_('You are not authorised to approve  or '
                                  'refuse this Timesheet.'))

    @api.multi
    def action_set_to_draft(self):
        self._check_authorised_validator()
        return super(HrTimesheetSheet, self).action_set_to_draft()

    @api.multi
    def action_done(self):
        self._check_authorised_validator()
        wf_service = netsvc.LocalService('workflow')
        for id in self.ids:
            wf_service.trg_validate(self.env.uid, 'hr_timesheet_sheet.sheet',
                                    id, 'done', self.env.cr)
        return True

    @api.multi
    def action_cancel(self):
        self._check_authorised_validator()
        wf_service = netsvc.LocalService('workflow')
        for id in self.ids:
            wf_service.trg_validate(self.env.uid, 'hr_timesheet_sheet.sheet',
                                    id, 'cancel', self.env.cr)
        return True
