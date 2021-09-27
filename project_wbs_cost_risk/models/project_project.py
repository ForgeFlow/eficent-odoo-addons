# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    budget_hours = fields.Float(related="analytic_account_id.budget_hours")

    @api.multi
    def _compute_planned_budget_hours(self):
        """Obtains the earliest and latest dates of the children."""
        for pp in self:
            budget_hours = 0
            for child in pp.child_ids:
                for project in child.project_ids:
                    budget_hours += project.budget_hours
            pp.write({"budget_hours": budget_hours})
        return True

    @api.multi
    def _propagate_budget_hours(self, vals):
        for pp in self:
            if "budget_hours" in vals:
                pp.analytic_account_id.write({"budget_hours": vals["budget_hours"]})

    @api.model
    def create(self, values):
        res = super(ProjectProject, self).create(values)
        res.parent_id.project_ids._compute_planned_budget_hours()
        res._propagate_budget_hours(values)
        return res

    @api.multi
    def write(self, vals):
        res = super(ProjectProject, self).write(vals)
        if "budget_hours" in vals:
            for pp in self:
                if not pp.parent_id:
                    return res
                pp.parent_id.project_ids._compute_planned_budget_hours()
                pp._propagate_budget_hours(vals)
        return res

    @api.multi
    def button_actual_hours(self):
        self.ensure_one()
        account = self.analytic_account_id
        domain = [
            ("account_id", "child_of", account.ids),
            ("sheet_id", "!=", False),
        ]
        analytic_line_obj = self.env["account.analytic.line"]
        anal_lines = analytic_line_obj.search(domain, order="id desc")
        action = self.env.ref("analytic.account_analytic_line_action_entries")
        result = action.read()[0]
        result["domain"] = "[('id','in',[" + ",".join(map(str, anal_lines.ids)) + "])]"
        result["context"] = {"group_by": ["user_id"]}
        return result
