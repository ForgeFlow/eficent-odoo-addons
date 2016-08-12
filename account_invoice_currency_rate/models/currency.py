# -*- coding: utf-8 -*-
# © 2015 Akretion, Benoît GUILLOT
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class ResCurrency(models.Model):
    _inherit = "res.currency"

    @api.multi
    def _get_current_rate(self, raise_on_no_rate=True):
        res = super(ResCurrency, self)._get_current_rate(
            raise_on_no_rate=raise_on_no_rate)

        for currency in self:
            if self.env.context.get('force_currency_rate', False) and not \
                    currency.base:
                res[currency.id] = self.env.context['force_currency_rate']
        return res
