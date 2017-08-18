# -*- coding: utf-8 -*-
# © 2014-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm


class AnalyticWipReport(orm.TransientModel):
    _inherit = 'analytic.wip.report'

    def _check_dates_within(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        obj = self.browse(cr, uid, ids[0], context=context)
        if obj.from_date_fy < obj.fiscalyear_id.date_start:
             return False
        if obj.to_date_fy > obj.fiscalyear_id.date_stop:
             return False
        if obj.to_date_fy < obj.from_date_fy:
            return False
        return True

    def analytic_wip_report_open_window(self, cr, uid, ids, context=None):
        res = super(AnalyticWipReport, self).analytic_wip_report_open_window(
            cr, uid, ids, context=context)
        data = self.read(cr, uid, ids, [])[0]
        result_context = {}
        if data['from_date']:
            result_context.update({'from_date': data['from_date']})
        if data['to_date']:
            result_context.update({'to_date': data['to_date']})
        if data['fiscalyear_id']:
            result_context.update({'fiscalyear_id': data['fiscalyear_id'][0]})
        if data['from_date_fy']:
            result_context.update({'from_date_fy': data['from_date_fy']})
        if data['to_date_fy']:
            result_context.update({'to_date_fy': data['to_date_fy']})
        res['context'] = str(result_context)
        return res

    _columns = {
        'fiscalyear_id': fields.many2one(
            'account.fiscalyear', 'Fiscalyear',
            required=True),
        'from_date_fy': fields.date('From (within the fiscal year)',
                                    required=True),
        'to_date_fy': fields.date('To (within the fiscal year)',
                                  required=True),
    }

    def onchange_fiscalyear_id(self, cr, uid, ids, fiscalyear_id, context=None):
        res = {}
        res['value'] = {}
        if context is None:
            context = {}
        if fiscalyear_id:
            fiscalyear = self.pool['account.fiscalyear'].browse(
                cr, uid, fiscalyear_id, context=context)
            res['value']['from_date_fy'] = fiscalyear.date_start
            res['value']['to_date_fy'] = fiscalyear.date_stop
        return res

    _constraints = [
        (_check_dates_within,
         'Error! fiscal year dates are wrong',
         ['from_date_fy', 'to_date_fy'])
    ]
