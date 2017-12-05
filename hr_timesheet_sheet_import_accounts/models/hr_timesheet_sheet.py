# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import _, api, exceptions, models
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet_sheet.sheet"

    @api.multi
    def set_previous_timesheet_ids(self):
        sheet_obj = self.env['hr_timesheet_sheet.sheet']
        timesheet_obj = self.env['account.analytic.line']
        for sheet in self:
            res = []
            date_from = datetime.strptime(sheet.date_from,
                                          DEFAULT_SERVER_DATE_FORMAT)
            user = self.env.user
            r = user.company_id and user.company_id.timesheet_range or 'month'
            delta = relativedelta(months=-1)
            if r == 'month':
                delta = relativedelta(months=-1)
            elif r == 'week':
                delta = relativedelta(weeks=-1)
            elif r == 'year':
                delta = relativedelta(years=-1)
            date_from_lw = (date_from + delta).strftime(
                DEFAULT_SERVER_DATE_FORMAT)
            emp_id = sheet.employee_id and sheet.employee_id.id or False
            if not emp_id:
                return False
            lw_sheet_ids = sheet_obj.search([
                ('date_to', '<=', date_from),
                ('date_from', '>=', date_from_lw),
                ('employee_id', '=', emp_id)])
            a_line_ids = lw_sheet_ids.mapped('timesheet_ids').ids
            ga_id = sheet.employee_id.product_id.\
                property_account_expense_id.id or \
                sheet.employee_id.product_id.\
                categ_id.property_account_expense_categ_id.id
            if not ga_id:
                raise exceptions.ValidationError(_(
                    'Please set a general expense '
                    'account in your employee view'))
            if a_line_ids:
                self.env.cr.execute("""SELECT DISTINCT L.account_id
                FROM account_analytic_line AS L
                WHERE L.id IN %s
                GROUP BY L.account_id""", (tuple(a_line_ids),))
                query = self.env.cr.dictfetchall()
                for account_id in [a['account_id'] for a in query]:
                    vals = {
                        'employee_id': sheet.employee_id.id,
                        'date': sheet.date_from,
                        'account_id': account_id,
                        'name': '/',
                        'product_id': sheet.employee_id.product_id.id,
                        'product_uom_id':
                            sheet.employee_id.product_id.uom_id.id,
                        'general_account_id': ga_id,
                        'user_id': self.env.user.partner_id.id,
                        'sheet_id': sheet.id,
                    }
                    ts_id = timesheet_obj.create(vals)
                res.append(ts_id.id)
        return {
            'domain': "[('id','in', [" + ','.join(map(str, res)) + "])]",
            'name': _('Employee Timesheets'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hr_timesheet_sheet.sheet',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }
