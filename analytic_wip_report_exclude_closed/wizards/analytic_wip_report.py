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

    def _get_analytic_search_domain(self, cr, uid, ids, data, context=None):
        data = self.read(cr, uid, ids, [])[0]
        comparing_date = False
        if context.get('fiscalyear_id', False):
            fiscalyear_id = context['fiscalyear_id']
            fiscalyear = self.pool.get('account.fiscalyear').browse(
                cr, uid, fiscalyear_id, context)
            comparing_date = fiscalyear.date_start

        if data['filter_project'] and data['filter_project'] == True \
                and comparing_date:
            domain = ['&', '|', '&', ('date', '>=', comparing_date),
                              ('state', '=', 'close'),
                              ('state', '!=', 'close'),
                              ('account_class', '=', 'project')]
        else:
            domain = ['|', '&', ('date', '>=', comparing_date),
                              ('state', '=', 'close'),
                              ('state', '!=', 'close')]
        return domain

    def analytic_wip_report_open_window(self, cr, uid, ids, context=None):
        res = super(AnalyticWipReport, self). \
            analytic_wip_report_open_window(cr, uid, ids, context=context)

        data = self.read(cr, uid, ids, [])[0]
        ctx = ast.literal_eval(res['context'])

        if not ctx.get('fiscalyear_id', False):
            return res
        res['domain'] = self._get_analytic_search_domain(cr, uid, ids, data,
                                                         ctx)
        return res
