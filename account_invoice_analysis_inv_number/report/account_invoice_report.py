# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"
    _auto = False

    number = fields.Char(
        'Invoice Number',
        size=32,
        readonly=True,
        help="""Unique number of the invoice, computed automatically when the
                invoice is created."""
    )
    reference = fields.Char(
        'Supplier Invoice Number',
        size=64,
        help="The reference of this invoice as provided by the supplier."
    )
    move_id = fields.Many2one(
        'account.move',
        'Journal Entry',
        readonly=True,
        size=64
    )

    _depends = {
        'account.invoice': [
            'account_id', 'amount_total_company_signed',
            'commercial_partner_id', 'company_id',
            'currency_id', 'date_due', 'date_invoice', 'fiscal_position_id',
            'journal_id', 'partner_bank_id', 'partner_id', 'payment_term_id',
            'residual', 'state', 'type', 'user_id', 'number', 'reference',
            'move_id'
        ],
        'account.invoice.line': [
            'account_id', 'invoice_id', 'price_subtotal', 'product_id',
            'quantity', 'uom_id', 'account_analytic_id',
        ],
        'product.product': ['product_tmpl_id'],
        'product.template': ['categ_id'],
        'product.uom': ['category_id', 'factor', 'name', 'uom_type'],
        'res.currency.rate': ['currency_id', 'name'],
        'res.partner': ['country_id'],
    }

    def _select(self):
        select_str = super(AccountInvoiceReport, self)._select()
        select_str += """, sub.number, sub.reference, sub.move_id"""
        return select_str

    def _sub_select(self):
        select_str = super(AccountInvoiceReport, self)._sub_select()
        select_str += """, ai.number, ai.reference, ai.move_id"""
        return select_str

    def _group_by(self):
        group_by_str = super(AccountInvoiceReport, self)._group_by()
        group_by_str += """, ai.number, ai.reference, ai.move_id"""
        return group_by_str
