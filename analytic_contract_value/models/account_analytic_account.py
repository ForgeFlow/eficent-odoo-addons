# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, orm
import openerp.addons.decimal_precision as dp


class AccountAnalyticAccount(orm.Model):
    _inherit = 'account.analytic.account'

    _columns = {
        'contract_value': fields.float(
            'Contract Value',
            digits_compute=dp.get_precision('Account'),
            track_visibility='onchange',
            readonly=True)
    }
