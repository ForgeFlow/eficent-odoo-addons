# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    @api.model
    def _compute_scheduled_dates(self, analytic):
        """Obtains the earliest and latest dates of the children."""
        start_dates = []
        end_dates = []
        if not analytic.child_ids:
            return True
        for child in analytic.child_ids:
            if child.date_start:
                start_dates.append(child.date_start)
            if child.date:
                end_dates.append(child.date)
        min_start_date = False
        max_end_date = False
        if start_dates:
            min_start_date = min(start_dates)
        if end_dates:
            max_end_date = max(end_dates)
        vals = {
            'date_start': min_start_date,
            'date': max_end_date,
        }
        analytic.write(vals)
        project_ids = self.env['project.project'].\
            search([('analytic_account_id', '=', analytic.id)])
        for project in project_ids:
            project.write(vals)
        return True

    date_start = fields.Date(
        'Start Date'
    )
    date = fields.Date(
        'Expiration Date',
        index=True,
        track_visibility='onchange'
    )

    @api.model
    def create(self, vals):
        acc = super(AccountAnalyticAccount, self).create(vals)
        self._compute_scheduled_dates(acc.parent_id)
        return acc

    @api.multi
    def write(self, vals):
        res = super(AccountAnalyticAccount, self).write(vals)
        if 'date_start' in vals or 'date' in vals:
            for acc in self:
                if not acc.parent_id:
                    return res
                self._compute_scheduled_dates(acc.parent_id)
        return res
