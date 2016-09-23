# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import decimal_precision as dp
from openerp.osv import fields, osv
from datetime import datetime
import ast


class AnalyticWipReport(osv.osv):
    _inherit = 'analytic.wip.report'

    _columns = {
        'filter_project': fields.boolean('Filter by project'),
    }
    _defaults = {
        'filter_project': True,
    }

    def analytic_wip_report_open_window(self, cr, uid, ids, context=None):
        res = super(AnalyticWipReport, self). \
            analytic_wip_report_open_window(cr, uid, ids, context=context)

        data = self.read(cr, uid, ids, [])[0]
        ctx = ast.literal_eval(res['context'])

        if ctx.get('fiscalyear_id', False):
            fiscalyear_id = ctx['fiscalyear_id']
            fiscalyear = self.pool.get('account.fiscalyear').browse(
                cr, uid, fiscalyear_id, context)
            comparing_date = fiscalyear.date_start
        else:
            return res

        if data['filter_project'] and data['filter_project'] == True:
            domain = unicode(['&', '|', '&', ('date', '>=', comparing_date),
                              ('state', '=', 'close'),
                              ('state', '!=', 'close'),
                              ('account_class', '=', 'project')])
        else:
            domain = unicode(['|', '&', ('date', '>=', comparing_date),
                              ('state', '=', 'close'),
                              ('state', '!=', 'close')])
        res['domain'] = domain
        return res
