# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from odoo import _, api, exceptions, models
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet_sheet.sheet"

    @api.multi
    def prepare_timesheet(self, project_id):
        for sheet in self:
            aa = self.env['project.project'].browse(
                project_id).analytic_account_id
            ga_id = self.env['account.analytic.line'].\
                _getGeneralAccountFromCostCategory(aa, sheet.user_id)
            if not ga_id:
                ga_id = sheet.employee_id.product_id.\
                    property_account_expense_id.id or \
                    sheet.employee_id.product_id.\
                    categ_id.property_account_expense_categ_id.id
            if not ga_id:
                raise exceptions.ValidationError(_(
                    'Please set a general expense '
                    'account in your employee view'))
            vals = {
                'date': sheet.date_from,
                'account_id': aa.id,
                'project_id': project_id,
                'name': '/',
                'product_id': sheet.employee_id.product_id.id,
                'product_uom_id':
                    sheet.employee_id.product_id.uom_id.id,
                'general_account_id': ga_id.id,
                'user_id': sheet.user_id.id,
                'sheet_id': sheet.id,
            }
            return vals

    @api.model
    def get_accounts(self, anal_line_ids):
        self.env.cr.execute("""SELECT DISTINCT L.project_id
        FROM account_analytic_line AS L
        INNER JOIN project_project PP ON L.project_id = PP.id
        WHERE L.id IN %s
        AND PP.allow_timesheets = true
        GROUP BY L.project_id""", (tuple(anal_line_ids),))
        return self.env.cr.dictfetchall()

    @api.model
    def get_sheet_domain(self, date_from, emp_id, period_type):
        return [('date_to', '<=', date_from),
                ('employee_id', '=', emp_id),
                ('hr_period_id.type_id', '=', period_type.id)]

    @api.multi
    def set_previous_timesheet_ids(self):
        sheet_obj = self.env['hr_timesheet_sheet.sheet']
        for sheet in self:
            if sheet.state not in ('draft', 'new'):
                raise exceptions.ValidationError(
                    _('Timesheet draft or opened'))
            date_from = datetime.strptime(sheet.date_from,
                                          DEFAULT_SERVER_DATE_FORMAT)
            emp_id = sheet.employee_id and sheet.employee_id.id or False
            if not emp_id:
                return False
            sheet_domain = self.get_sheet_domain(
                date_from, emp_id, sheet.hr_period_id.type_id)
            lw_sheet_ids = sheet_obj.search(
                sheet_domain, limit=1, order='date_to desc')
            a_line_ids = lw_sheet_ids.mapped('timesheet_ids').ids
            if a_line_ids:
                projects = self.get_accounts(a_line_ids)
                for project_id in [a['project_id'] for a in projects]:
                    vals = sheet.prepare_timesheet(project_id)
                    self.env['account.analytic.line'].create(vals)
        return True
