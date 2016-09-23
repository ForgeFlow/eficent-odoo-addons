# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import decimal_precision as dp
from openerp.osv import fields, osv
from datetime import datetime
import ast

class AnalyticWipReport(osv.osv):
    
    _inherit = 'analytic.wip.report'

    def analytic_wip_report_open_window(self, cr, uid, ids, context=None):
        res = super(AnalyticWipReport, self). \
            analytic_wip_report_open_window(cr, uid, ids, context=context)

        ctx = ast.literal_eval(res['context'])

        if ctx.get('fiscalyear_id', False):
            fiscalyear_id = ctx['fiscalyear_id']
            fiscalyear = self.pool.get('account.fiscalyear').browse(
                cr, uid, fiscalyear_id, context)
            comparing_date = fiscalyear.date_start
        else:
            return res
        domain = unicode(['|', ('date', '>=', comparing_date), ('date', '=',
                                                                False)])
        res['domain'] = domain
        return res
