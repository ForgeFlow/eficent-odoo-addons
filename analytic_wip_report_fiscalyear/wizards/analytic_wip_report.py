# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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
from openerp.osv import fields, orm


class AnalyticWipReport(orm.TransientModel):
    _inherit = 'analytic.wip.report'

    _columns = {
        'fiscalyear_id': fields.many2one(
                'account.fiscalyear', 'Fiscalyear',
                required=True),
    }

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
        res['context'] = str(result_context)
        return res
