from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet.sheet"

    @api.model
    def _default_department(self):
        employees = self.env["hr.employee"].search(
            [("user_id", "=", self.env.uid)]
        )
        for emp in employees:
            return emp.department_id and emp.department_id.id or False
        return False

    validator_user_ids = fields.Many2many("res.users", string="Validators")

    department_id = fields.Many2one(
        comodel_name="hr.department",
        string="Department",
        default=_default_department,
    )

    @api.model
    def create(self, vals):
        employee_id = vals.get("employee_id", False)
        if employee_id:
            employee = self.env["hr.employee"].browse(employee_id)
            validators = employee.get_validator_user_ids()
            vals["validator_user_ids"] = [
                (4, user_id) for user_id in validators
            ]
        return super(HrTimesheetSheet, self).create(vals)

    @api.multi
    def _check_authorised_validator(self):
        for timesheet in self.filtered(
                lambda ts: ts.company_id.use_timesheet_validators):
            if not self.env.user._is_superuser():
                if self.env.uid not in timesheet.validator_user_ids.ids:
                    raise UserError(
                        _(
                            "You are not authorised to approve  or "
                            "refuse this Timesheet."
                        )
                    )

    @api.multi
    def action_timesheet_draft(self):
        self._check_authorised_validator()
        return super(HrTimesheetSheet, self).action_timesheet_draft()

    @api.multi
    def action_timesheet_done(self):
        self._check_authorised_validator()
        return super(HrTimesheetSheet, self).action_timesheet_done()
