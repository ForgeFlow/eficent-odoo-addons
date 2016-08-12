# -*- coding: utf-8 -*-
# © 2015 Akretion, Benoît GUILLOT
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    @api.one
    def _show_force_currency(self):
        if self.state == 'draft':
            if self.currency_id.id == self.company_id.currency_id.id:
                self.show_force_currency = False
            else:
                self.show_force_currency = True
        else:
            self.show_force_currency = False

    currency_rate = fields.Float('Forced currency rate',
                                 help="You can force the currency rate on the "
                                      "invoice with this field.",
                                 track_visibility='always', readonly=True)
    show_force_currency = fields.Boolean(compute="_show_force_currency",
                                         string="Show force currency")

    @api.one
    @api.depends('currency_rate')
    def _currency_rate_onchange(self):
        self.button_compute(set_total=False)

    @api.one
    @api.depends('currency_rate')
    def _compute_residual(self):
        if self.currency_rate:
            obj = self.with_context(force_currency_rate=self.currency_rate)
        else:
            obj = self
        super(AccountInvoice, obj)._compute_residual()

    @api.multi
    def action_move_create(self):
        if self.currency_rate:
            obj = self.with_context(force_currency_rate=self.currency_rate)
        else:
            obj = self
        super(AccountInvoice, obj).action_move_create()

    @api.multi
    def _get_analytic_lines(self):
        if self.currency_rate:
            obj = self.with_context(
                    force_currency_rate=self.currency_rate)
        else:
            obj = self
        return super(AccountInvoice, obj)._get_analytic_lines()

    @api.multi
    def compute_invoice_totals(self, company_currency, ref, invoice_move_lines):
        if self.currency_rate:
            obj = self.with_context(
                    force_currency_rate=self.currency_rate)
        else:
            obj = self
        return super(AccountInvoice, obj).compute_invoice_totals(
                company_currency, ref, invoice_move_lines)


class AccountInvoiceTax(models.Model):

    _inherit = "account.invoice.tax"

    @api.v8
    def compute(self, invoice):
        if invoice.currency_rate:
            invoice = invoice.with_context(
                    force_currency_rate=invoice.currency_rate)
        return super(AccountInvoiceTax, self).compute(invoice)

    @api.multi
    def base_change(self, base, currency_id=False, company_id=False, date_invoice=False):
        return {'value': {}}

    @api.multi
    def amount_change(self, amount, currency_id=False, company_id=False, date_invoice=False):
        return {'value': {}}

    @api.one
    @api.onchange('base', 'invoice_id.currency_id', 'invoice_id.company_id')
    def onchange_base(self):
        factor = self.factor_base if self else 1
        company = self.env['res.company'].browse(self.invoice_id.company_id)
        if self.invoice_id.currency_id and \
                self.invoice_id.company_id.currency_id:
            currency = self.env['res.currency'].browse(
                    self.invoice_id.currency_id)
            if self.invoice_id.currency_rate:
                currency = currency.with_context(
                        force_currency_rate=self.invoice_id.currency_rate)
            currency = currency.with_context(
                    date=self.invoice_id.date_invoice or
                         fields.Date.context_today(self))
            self.base_amount = currency.compute(self.base * factor,
                                                company.currency_id,
                                                round=False)

    @api.one
    @api.onchange('amount', 'invoice_id.currency_id', 'invoice_id.company_id')
    def onchange_amount(self):
        company = self.env['res.company'].browse(self.invoice_id.company_id)
        if self.invoice_id.currency_id and \
                self.invoice_id.company_id.currency_id:
            currency = self.env['res.currency'].browse(
                    self.invoice_id.currency_id)
            if self.invoice_id.currency_rate:
                currency = currency.with_context(
                        force_currency_rate=self.invoice_id.currency_rate)
            currency = currency.with_context(
                    date=self.invoice_id.date_invoice or
                         fields.Date.context_today(self))
            amount = currency.compute(self.amount, company.currency_id,
                                      round=False)
        tax_sign = (self.tax_amount / self.amount) if self.amount else 1
        self.tax_amount = amount * tax_sign


class AccountInvoiceLine(models.Model):

    _inherit = "account.invoice.line"

    @api.model
    def move_line_get(self, invoice_id):
        if self.invoice_id and self.invoice_id.currency_rate:
            obj = self.with_context(
                    force_currency_rate=self.invoice_id.currency_rate)
        else:
            obj = self
        return super(AccountInvoiceLine, obj).move_line_get(invoice_id)
