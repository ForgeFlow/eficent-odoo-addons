# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models, _


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    @api.multi
    def onchange_filter(self, filter):
        to_clean = super(StockInventory, self).onchange_filter(filter)
        for record in self:
            if filter != 'analytic':
                to_clean['value']['analytic_account_id'] = False
            return to_clean

    @api.model
    def _get_available_filters(self):
        """This function will return the list of filters allowed according to
        the options checked in 'Settings/Warehouse'.

        :return: list of tuple
        """
        res_filters = super(StockInventory, self)._get_available_filters()
        res_filters.append(('analytic', _('One Analytic Account')))
        return res_filters

    filter = fields.Selection(
        selection=_get_available_filters, string='Selection Filter',
        required=True)
