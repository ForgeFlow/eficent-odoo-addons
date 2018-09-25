# -*- coding: utf-8 -*-
# Copyright 2018 Odoo SA
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lpgl.html).

from odoo import models, api
from odoo.tools.float_utils import float_round
from odoo.exceptions import UserError


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    @api.multi
    def auto_reconcile(self):
        # Copying standard as impossible to change behavior otherwise.
        # The changes are at XXX
        self.ensure_one()
        match_recs = self.env['account.move.line']

        amount = self.amount_currency or self.amount
        company_currency = self.journal_id.company_id.currency_id
        st_line_currency = self.currency_id or self.journal_id.currency_id
        currency = (st_line_currency and
                    st_line_currency != company_currency) and \
            st_line_currency.id or False
        precision = (st_line_currency and st_line_currency.decimal_places
                     or company_currency.decimal_places)
        # XXX parse check number
        labels = self.name.split('/')
        ref = tuple(int(s) for s in labels if s.isdigit())
        params = {
            'company_id': self.env.user.company_id.id,
            'account_payable_receivable': (
                self.journal_id.default_credit_account_id.id,
                self.journal_id.default_debit_account_id.id),
            'amount': float_round(amount, precision_digits=precision),
            'partner_id': self.partner_id.id,
            'ref': ref,
        }
        field = currency and 'amount_residual_currency' or 'amount_residual'
        liquidity_field = (currency and 'amount_currency' or amount > 0
                           and 'debit' or 'credit')
        # XXX check check number not just the JE number
        if ref:
            sql_query = self._get_common_sql_query() + \
                " AND aml.check_number in %(ref)s AND ("+field + \
                " = %(amount)s OR (acc.internal_type = 'liquidity'" \
                "AND "+liquidity_field+" = %(amount)s)) \
                ORDER BY date_maturity asc, aml.id asc"
            self.env.cr.execute(sql_query, params)
            match_recs = self.env.cr.dictfetchall()
            if len(match_recs) > 1:
                return False

        # XXX  Deleting lines here. Do not reconcile if no cehck found
        if not match_recs:
            return False

        match_recs = self.env['account.move.line'].browse(
            [aml.get('id') for aml in match_recs])
        # Now reconcile
        counterpart_aml_dicts = []
        payment_aml_rec = self.env['account.move.line']
        for aml in match_recs:
            if aml.account_id.internal_type == 'liquidity':
                payment_aml_rec = (payment_aml_rec | aml)
            else:
                amount = (aml.currency_id and
                          aml.amount_residual_currency or aml.amount_residual)
                counterpart_aml_dicts.append({
                    'name': aml.name if aml.name != '/' else aml.move_id.name,
                    'debit': amount < 0 and -amount or 0,
                    'credit': amount > 0 and amount or 0,
                    'move_line': aml
                })

        try:
            with self._cr.savepoint():
                counterpart = self.process_reconciliation(
                    counterpart_aml_dicts=counterpart_aml_dicts,
                    payment_aml_rec=payment_aml_rec)
            return counterpart
        except UserError:
            self.invalidate_cache()
            self.env['account.move'].invalidate_cache()
            self.env['account.move.line'].invalidate_cache()
            return False
