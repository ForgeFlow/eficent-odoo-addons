# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent
#    (<http://www.eficent.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
from openerp import tools
from openerp.osv import fields, osv, orm


class TimesheetReport(orm.Model):
    _inherit = "timesheet.report"
    _columns = {
        'project_analytic_account_id': fields.many2one(
            'account.analytic.account', 'Root Project', readonly=True),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'timesheet_report')
        cr.execute("""
            create or replace view timesheet_report as (
                    select
                        min(aal.id) as id,
                        htss.name,
                        aal.date as date,
                        htss.date_from,
                        htss.date_to,
                        to_char(htss.date_from, 'YYYY-MM-DD') as day,
                        to_char(htss.date_from, 'YYYY') as year,
                        to_char(htss.date_from, 'MM') as month,
                        count(*) as nbr,
                        aal.unit_amount as quantity,
                        aal.amount as cost,
                        aal.account_id,
                        a.project_analytic_account_id,
                        aal.product_id,
                        (SELECT   sum(day.total_difference)
                            FROM hr_timesheet_sheet_sheet AS sheet 
                            LEFT JOIN hr_timesheet_sheet_sheet_day AS day 
                            ON (sheet.id = day.sheet_id) where sheet.id=htss.id) as total_diff,
                        (SELECT sum(day.total_timesheet)
                            FROM hr_timesheet_sheet_sheet AS sheet 
                            LEFT JOIN hr_timesheet_sheet_sheet_day AS day 
                            ON (sheet.id = day.sheet_id) where sheet.id=htss.id) as total_timesheet,
                        (SELECT sum(day.total_attendance)
                            FROM hr_timesheet_sheet_sheet AS sheet 
                            LEFT JOIN hr_timesheet_sheet_sheet_day AS day 
                            ON (sheet.id = day.sheet_id) where sheet.id=htss.id) as total_attendance,
                        aal.to_invoice,
                        aal.general_account_id,
                        htss.user_id,
                        htss.company_id,
                        htss.department_id,
                        htss.state
                    from account_analytic_line as aal
                    inner join account_analytic_account a on (aal.account_id = a.id)
                    left join hr_analytic_timesheet as hat ON (hat.line_id=aal.id)
                    left join hr_timesheet_sheet_sheet as htss ON (hat.sheet_id=htss.id)
                    group by
                        aal.account_id,
                        a.project_analytic_account_id,
                        aal.date,
                        htss.date_from,
                        htss.date_to,
                        aal.unit_amount,
                        aal.amount,
                        aal.to_invoice,
                        aal.product_id,
                        aal.general_account_id,
                        htss.name,
                        htss.company_id,
                        htss.state,
                        htss.id,
                        htss.department_id,
                        htss.user_id
            )
        """)
