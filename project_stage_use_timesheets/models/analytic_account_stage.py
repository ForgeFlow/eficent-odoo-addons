# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AnalyticAccountStage(models.Model):
    _inherit = 'analytic.account.stage'

    allow_timesheets = fields.Boolean(
        'Timesheets', default=True,
        help="Check this field if setting this stage should make the project"
             " to manage timesheets")
