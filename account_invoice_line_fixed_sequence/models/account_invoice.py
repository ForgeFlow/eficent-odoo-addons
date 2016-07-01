# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def _reset_sequence(self):
        for rec in self:
            current_sequence = 1
            for line in rec.move_lines:
                line.write({'sequence': current_sequence})
                current_sequence += 1

    # reset line sequence number during write
    @api.multi
    def write(self, line_values):
        if isinstance(self, (int, long)):
            ids = [self]
        res = super(AccountInvoice, self).write(line_values)
        self._reset_sequence()
        return res


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    sequence = fields.Integer('Sequence',
                                   help="Gives the sequence "
                                        "order when displaying a list of "
                                        "invoice lines.",
                                   default=99999)

    @api.model
    def create(self, values):
        line_id = super(AccountInvoiceLine, self).create(values)
        if 'invoice_id' in values and values['invoice_id']:
            self.env['account.invoice'].browse(values['invoice_id'])._reset_sequence()
        return line_id
