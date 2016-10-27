# -*- coding: utf-8 -*-
# © 2016 - Eficent http://www.eficent.com/
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.multi
    def _check_type(self):
        for rec in self:
            if rec.analytic_account_id:
                if rec.account_id.user_type.report_type \
                        not in ('income', 'expense'):
                    rec.valid_to_post = False
                    continue
            rec.valid_to_post = True

    valid_to_post = fields.Boolean('Entry allowed to be post',
                                   compute='_check_type')

    @api.cr_uid_ids_context
    def create_analytic_lines(self, cr, uid, ids, context=None):
        valid_entries = []
        for line in self.browse(cr, uid, ids, context=context):
            if line.valid_to_post:
                valid_entries.append(line.id)
        return super(AccountMoveLine, self).create_analytic_lines(cr, uid,
            valid_entries, context)
