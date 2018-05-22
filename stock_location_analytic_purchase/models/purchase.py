# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm
from openerp.tools.translate import _


class PurchaseOrderLine(orm.Model):
    _inherit = "purchase.order.line"

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
                          'destiantion location and PO line have to match')
                    )
        return super(PurchaseOrderLine, self).action_confirm(cr, uid, ids,
                                                             context)
