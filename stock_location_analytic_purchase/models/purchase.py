# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm
from openerp.tools.translate import _


class PurchaseOrderLine(orm.Model):
    _inherit = "purchase.order.line"

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        res = super(PurchaseOrderLine, self).create(cr, uid, vals, context)
        if vals.get('account_analytic_id'):
            account_analytic_id = vals['account_analytic_id']
            location_id = self.pool.get('stock.location').search(
                cr, uid, [('analytic_account_id', '=', account_analytic_id)])
            if len(location_id):
                for line in self.browse(cr, uid, [res], context):
                    if line.order_id:
                        self.pool.get('purchase.order').write(cr, uid, line.order_id.id, {'location_id': location_id[0]})

        return res

    def action_confirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context):
            loc_analytic_account = line.order_id.location_id.analytic_account_id
            if line.account_analytic_id:
                if line.account_analytic_id != loc_analytic_account:
                    raise orm.except_orm(
                        _('Error'),
                        _('The analytic account in the location and in the '
                          'destination location and PO line have to match')
                    )
        return super(PurchaseOrderLine, self).action_confirm(cr, uid, ids,
                                                             context)
