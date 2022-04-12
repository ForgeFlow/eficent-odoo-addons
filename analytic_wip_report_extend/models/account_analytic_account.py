# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import odoo.addons.decimal_precision as dp
from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    @api.multi
    def _compute_wip_report(self):
        res = super(AccountAnalyticAccount, self)._compute_wip_report()
        for account in self:
            # Estimated gross profit percentage
            try:
                account.estimated_gross_profit_per = (
                    account.estimated_gross_profit /
                    account.total_value * 100)
            except ZeroDivisionError:
                account.estimated_gross_profit_per = 0
            # Over/Under billings
            over_under_billings =\
                account.under_billings - account.over_billings
            account.under_over = over_under_billings

            # # PAID Analytic Line
            # the problem is receivable lines without analytic account
            # that was before I introduce the hack into Odoo for that. So I have
            # to go to the invoice and then the lines
            actual_paid_line_ids = []
            invoices = []
            for line_id in account.actual_billings_line_ids:
                invoice = line_id.move_id.move_id
                if not invoice:
                    continue
                if invoice in invoices:
                    # several income lines in the same invoice, do not count it twice
                    continue
                invoices.append(invoice)
                # issue if invoices are mixing projects but that is the best
                # I can do as long old receivable lines are not attached to projects
                rec_lines = invoice.mapped("line_ids").filtered(lambda l: 'Receivable' in l.account_id.user_type_id.name)
                account.actual_paid += sum([l.balance for l in rec_lines])
                # the total paid is the balance less the residual amount
                rec_lines_company_curr = rec_lines.filtered(lambda l: not l.currency_id)
                account.actual_paid -= sum(rec_lines_company_curr.mapped("amount_residual"))
                rec_lines_other_curr = rec_lines.filtered(lambda l: l.currency_id)
                account.actual_paid -= sum(rec_lines_other_curr.mapped("amount_residual_currency"))
                actual_paid_line_ids.extend(rec_lines.ids)

            account.actual_paid_line_ids = [
                (6, 0, [l for l in actual_paid_line_ids])]
        return res

    estimated_gross_profit_per = fields.Float(
        compute='_compute_wip_report',
        string='Total Value',
        help="""Estimated gros profit percentage
             (estimated gross profit/total contract value)""",
        digits=dp.get_precision('Account')
    )
    under_over = fields.Float(
        compute='_compute_wip_report',
        help="""Total under/over (under_billed-over_billed)"""
    )
    actual_paid = fields.Float(
        compute='_compute_wip_report',
        string='Paid to date',
        help="""Total paid amount from the customer to date""",
        digits=dp.get_precision('Account')
    )
    actual_paid_line_ids = fields.Many2many(
        comodel_name="account.analytic.line",
        compute='_compute_wip_report',
        string='Detail',
    )

    @api.multi
    def action_open_move_lines(self):
        line = self
        bill_lines = [x.id for x in line.actual_paid_line_ids]
        res = self.env['ir.actions.act_window'].for_xml_id(
            'account', 'action_account_moves_all_a')
        res['domain'] = "[('id', 'in', ["+','.join(
            map(str, bill_lines))+"])]"
        return res
