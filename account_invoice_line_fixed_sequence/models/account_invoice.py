# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, osv, orm
import logging

_logger = logging.getLogger(__name__)


class AccountInvoice(orm.Model):
    _inherit = 'account.invoice'

    def _reset_sequence(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for rec in self.browse(cr, uid, ids, context=context):
            current_sequence = 1
            for line in rec.move_lines:
                line.write({'sequence': current_sequence})
                current_sequence += 1

    # reset line sequence number during write
    def write(self, cr, uid, ids, line_values, context=None):
        if context is None:
            context = {}
        res = super(AccountInvoice, self).write(cr, uid, ids, line_values,
                                                context=context)
        self._reset_sequence(cr, uid, ids, context=context)
        return res


class AccountInvoiceLine(orm.Model):
    _inherit = 'account.invoice.line'

    _columns = {
        'sequence': fields.integer('Sequence',
                                   help="Gives the sequence "
                                        "order when displaying a list of "
                                        "invoice lines.",
                                   default=99999)
    }

    def create(self, cr, uid, values, context=None):
        if context is None:
            context = {}
        line_id = super(AccountInvoiceLine, self).create(cr, uid, values,
                                                         context=context)
        if 'invoice_id' in values and values['invoice_id']:
            self.pool['account.invoice']._reset_sequence(cr, uid,
                                                       [values['invoice_id']],
                                                       context=context)
        return line_id
