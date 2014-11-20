# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
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

from openerp.osv import fields, osv


class purchase_requisition(osv.osv):
    _inherit = "purchase.requisition"

    _columns = {
        'account_analytic_ids': fields.related('line_ids',
                                               'account_analytic_id',
                                               type='many2many',
                                               relation='account.analytic.account',
                                               string='Analytic Account',
                                               readonly=True),
        'account_analytic_user_ids': fields.related('line_ids',
                                                    'account_analytic_user_id',
                                                    type='many2many',
                                                    relation='res.users',
                                                    string='Project Manager',
                                                    readonly=True),
    }    

    def make_purchase_order(self, cr, uid, ids, partner_id, context=None):

        if context is None:
            context = {}
        res = super(purchase_requisition, self).make_purchase_order(cr, uid, ids, partner_id, context=context)

        pol_obj = self.pool.get('purchase.order.line')
        po_obj = self.pool.get('purchase.order')

        for requisition in self.browse(cr, uid, ids, context=context):
            po_req = po_obj.search(cr, uid, [('requisition_id', '=', requisition.id)], context=context)
            for po_id in po_req:
                pol_ids = pol_obj.search(cr, uid, [('order_id', '=', po_id)])
                for pol_id in pol_ids:
                    pol_brw = pol_obj.browse(cr, uid, pol_id)
                    pol_obj.write(cr, uid, [pol_brw.id], {'account_analytic_id':
                        pol_brw.purchase_requisition_line_id.account_analytic_id.id}, context=context)
        return res

purchase_requisition()
