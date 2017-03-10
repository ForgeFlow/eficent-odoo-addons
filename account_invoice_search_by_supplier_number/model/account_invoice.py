# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import osv, fields


class AccountInvoice(osv.osv):
    _inherit = 'account.invoice'

    def name_search(self, cr, user, name, args=None, operator='ilike',
                    context=None, limit=100):

        if not args:
            args = []
        if name:
            ids = self.search(cr, user, [(
                'supplier_invoice_number', operator, name)] + args,
                              limit=limit, context=context)
            ids2 = self.search(cr, user, [
                ('number', operator, name)] + args, limit=limit,
                context=context)
            if ids2:
                ids.extend(ids2)
                ids = list(set(ids))
            if not ids:
                ids = set()
                ids.update(map(lambda a: a[0],
                               super(AccountInvoice, self).name_search(
                                   cr, user, name=name, args=args,
                                   operator=operator,
                                   context=context, limit=limit)))
                ids = list(ids)
        else:
            ids = self.search(cr, user, args, limit=limit, context=context)
        context.update(show_supplier_ref=True)
        result = self.name_get(cr, user, ids, context=context)
        return result

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = []
        if not context.get('show_supplier_ref', True):
            return super(AccountInvoice, self).name_get(cr, uid, ids, context)
        else:
            for value in self.browse(cr, uid, ids, context=context):
                res.append([value.id, "%s: %s" % (
                    value.number, value.supplier_invoice_number)])
        return res
