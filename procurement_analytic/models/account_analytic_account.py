# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    procurement_ids = fields.One2many(
        comodel_name='procurement.order',
        inverse_name='analytic_account_id',
        string='Procurement Orders',
        copy=False)
