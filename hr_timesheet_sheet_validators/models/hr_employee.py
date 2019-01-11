# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.multi
    def get_validator_user_ids(self):
        """Return the list of user_ids that can validate a given timesheet."""
        self.ensure_one()
        for employee in self:
            users = []
            if (employee and
                    employee.parent_id and
                    employee.parent_id.user_id):
                users.append(
                    employee.parent_id.user_id.id)
            if (employee.department_id and
                    employee.department_id.manager_id and
                    employee.department_id.manager_id.user_id and
                    employee.department_id.manager_id.user_id.id !=
                    self.env.uid):
                users.append(
                    employee.department_id.manager_id.user_id.id)
            elif (employee.department_id and
                  employee.department_id.parent_id and
                  employee.department_id.parent_id.manager_id and
                  employee.department_id.parent_id.manager_id.user_id and
                  employee.department_id.parent_id.manager_id.user_id.id !=
                  self.env.uid):
                users.append(
                    employee.department_id.manager_id.user_id.id)
            return list(set(users)) if users else []
