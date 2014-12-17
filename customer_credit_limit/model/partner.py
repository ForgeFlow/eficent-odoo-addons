# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm, fields
from openerp.tools.translate import _


class res_partner(orm.Model):
    _inherit = "res.partner"

    def _total_exposure(self, cr, uid, ids, field_names, arg, context=None):
        currency_obj = self.pool.get('res.currency')
        res = {}
        for partner in self.browse(cr, uid, ids, context=context):
            credit = partner.credit
            debit = partner.debit
            # We sum from all the sale orders that are approved,
            # the sale order lines that are not yet invoiced
            order_obj = self.pool.get('sale.order')
            filters = [('partner_id', '=', partner.id),
                       ('state', '<>', 'draft'),
                       ('state', '<>', 'cancel'),
                       ('state', '<>', 'sent')]
            approved_order_ids = order_obj.search(
                cr, uid, filters, context=context)
            approved_orders_amount = 0.0
            for order in order_obj.browse(
                    cr, uid, approved_order_ids, context=context):
                for order_line in order.order_line:
                    if not order_line.invoiced:
                        if order.currency_id.id != \
                                order.company_id.currency_id.id:
                            so_line_total_cc = currency_obj.compute(
                                cr, uid, order.currency_id.id,
                                order.company_id.currency_id.id,
                                order_line.price_subtotal, context=context)
                            approved_orders_amount += so_line_total_cc
                        else:
                            approved_orders_amount += \
                                order_line.price_subtotal

            # We sum from all the invoices
            # that are in draft the total amount
            invoice_obj = self.pool.get('account.invoice')
            filters = [('partner_id', '=', partner.id),
                       ('state', '=', 'draft'),
                       ('type', 'in', ('in_invoice', 'out_refund'))]
            draft_invoices_ids = invoice_obj.search(
                cr, uid, filters, context=context)
            draft_invoices_debit = 0.0
            for invoice in invoice_obj.browse(
                    cr, uid, draft_invoices_ids, context=context):
                if invoice.currency_id.id != \
                        invoice.company_id.currency_id.id:
                    inv_total_cc = currency_obj.compute(
                        cr, uid, order.currency_id.id,
                        order.company_id.currency_id.id,
                        invoice.amount_total, context=context)
                    draft_invoices_debit += inv_total_cc
                else:
                    draft_invoices_debit += invoice.amount_total

            # We sum from all the refund customer invoices
            # that are in draft the total amount
            filters = [('partner_id', '=', partner.id),
                       ('state', '=', 'draft'),
                       ('type', 'in', ('in_refund', 'out_invoice'))]
            draft_invoices_ids = invoice_obj.search(
                cr, uid, filters, context=context)
            draft_invoices_credit = 0.0
            for invoice in invoice_obj.browse(
                    cr, uid, draft_invoices_ids, context=context):
                if invoice.currency_id.id != invoice.company_id.currency_id.id:
                    inv_total_cc = currency_obj.compute(
                        cr, uid, order.currency_id.id,
                        order.company_id.currency_id.id,
                        invoice.amount_total, context=context)
                    draft_invoices_credit += inv_total_cc
                else:
                    draft_invoices_credit += invoice.amount_total

            total_exposure = credit \
                - debit \
                + approved_orders_amount \
                + draft_invoices_credit \
                - draft_invoices_debit
            res[partner.id] = total_exposure
        return res
    _columns = {
        'total_credit_exposure': fields.function(
            _total_exposure, string='Total Credit Exposure',
            help="Open transactions with the partner relevant for "
                 "credit limit, on a specified date."
                 "A positive value means that the company owes to the "
                 "partner."),

    }

