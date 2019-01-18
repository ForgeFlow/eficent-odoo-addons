# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, _
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def _get_timesheet_cost(self, values):
        res = super(AccountAnalyticLine, self)._get_timesheet_cost(values)
        if not values.get('journal_id', False):
            labor_anal_journal = self.env['account.analytic.journal'].search(
                [('cost_type', '=', 'labor')], limit=1)
            if not labor_anal_journal:
                raise ValidationError(
                    _("Please create an analytic journal for labor cost"))
            res['journal_id'] = labor_anal_journal.id
        return res
