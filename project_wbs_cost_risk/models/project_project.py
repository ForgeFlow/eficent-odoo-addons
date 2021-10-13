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
        all_ids = account.get_child_accounts().keys()
        query_params = [tuple(all_ids)]
        cr = self._cr
        cr.execute(
            """
            SELECT L.id
            FROM account_analytic_line AS L
            LEFT JOIN account_analytic_account AS A
            ON L.account_id = A.id
            INNER JOIN account_analytic_journal AS AAJ
            ON AAJ.id = L.journal_id
            AND AAJ.cost_type = 'labor'
            INNER JOIN account_account AC
            ON L.general_account_id = AC.id
            INNER JOIN account_account_type AT
            ON AT.id = AC.user_type_id
            WHERE AT.name in ('Expense', 'Cost of Goods Sold',
            'Expenses', 'Cost of Revenue')
            AND L.account_id IN %s
            """,
            query_params
        )
        anal_lines = [r[0] for r in cr.fetchall()]
        action = self.env.ref("analytic.account_analytic_line_action_entries")
        result = action.read()[0]
        result["domain"] = "[('id','in',[" + ",".join(map(str, anal_lines)) + "])]"
        result["context"] = {"group_by": ["user_id"]}
        return result
