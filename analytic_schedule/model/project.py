# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    @api.multi
    def _compute_scheduled_dates(self):
        """Obtains the earliest and latest dates of the children."""
        for pp in self:
            start_dates = []
            end_dates = []
            for child in pp.child_ids:
                for project in child.project_ids:
                    if project.date_start:
                        start_dates.append(project.date_start)
                    if project.date:
                        end_dates.append(project.date)
            min_start_date = False
            max_end_date = False
            if start_dates:
                min_start_date = min(start_dates)
            if end_dates:
                max_end_date = max(end_dates)
            if min_start_date and max_end_date:
                pp.write({'date_start': min_start_date, 'date': max_end_date})
            elif min_start_date:
                pp.write({'date_start': min_start_date})
            elif max_end_date:
                pp.write({'date': max_end_date})
        return True

    @api.multi
    def propagate_dates(self, vals):
        for rec in self:
            if "date_start" in vals and "date" in vals:
                for pp in rec:
                    pp.analytic_account_id.write(
                        {
                            "date_start": vals["date_start"],
                            "date": vals["date"],
                        }
                    )
            elif "date" in vals:
                for pp in rec:
                    pp.analytic_account_id.write(
                        {"date": vals["date"]}
                    )
            elif "date_start" in vals:
                for pp in rec:
                    pp.analytic_account_id.write(
                        {"date_start": vals["date_start"]}
                    )

    @api.model
    def create(self, values):
        res = super(ProjectProject, self).create(values)
        res.parent_id.project_ids._compute_scheduled_dates()
        res.propagate_dates(values)
        return res

    @api.multi
    def write(self, vals):
        res = super(ProjectProject, self).write(vals)
        if "date_start" in vals or "date" in vals:
            for pp in self:
                pp.parent_id.project_ids._compute_scheduled_dates()
                pp.propagate_dates(vals)
                if not pp.parent_id:
                    return res
        return res
