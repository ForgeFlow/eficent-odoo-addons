# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
import odoo.addons.decimal_precision as dp


class AnalyticChangeContractValue(models.TransientModel):
    _name = "analytic.change.contract.value"
    _description = "Change Contract Value"
    new_value = fields.Float('New Contract Value',
                             digits=dp.get_precision('Account'),
                             required=True)

    @api.multi
    def change_contract_value(self):
        self.ensure_one()
        rec_id = context and context.get('active_id', False)
        assert rec_id, _('Active ID is not set in Context')
        aa = self.env['account.analytic_account'].browse(rec_id)
        aa.write({'contract_value': self.new_value})
        return {}
