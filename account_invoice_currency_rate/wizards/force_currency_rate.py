# -*- coding: utf-8 -*-
# © 2015 Akretion, Benoît GUILLOT
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class InvoiceForceCurrencyRate(models.TransientModel):
    _name = "invoice.force.currency.rate"
    _description = "Force currency rate"

    @api.model
    def _get_currency_rate(self):
        rate = 1
        if self.env.context.get('active_id', False):
            invoice = self.env['account.invoice'].browse(
                    self.env.context.get('active_id'))
            rate = invoice.currency_id.rate
        return rate

    currency_rate = fields.Float('Forced currency rate',
                                 help="You can force the currency rate on "
                                      "the invoice with this field.",
                                 default=_get_currency_rate)

    @api.multi
    def force_currency_rate(self):
        if self.env.context.get('active_id', False):
            invoice = self.env['account.invoice'].browse(
                    self.env.context['active_id'])
            invoice.write({'currency_rate': self.currency_rate})
            invoice.button_compute(set_total=False)
        return {'type': 'ir.actions.act_window_close'}
