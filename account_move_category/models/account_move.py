# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm


class AccountMove(orm.Model):
    _inherit = "account.move"

    _columns = {
        'category': fields.selection(
            [('normal', 'Normal'),
             ('open', 'Opening Fiscal year'),
             ('close', 'Closing Fiscal Year')],
            'Category', select=True),
    }

    # def _prepare_analytic_line(self, cr, uid, obj_line, context=None):
    #     res = super(AccountMove, self)._prepare_analytic_line(
    #         cr, uid, obj_line, context)
    #     line = self.browse(cr, uid, obj_line, context=context)
    #     res.update(category_id=line.category_id)
    #     return res
