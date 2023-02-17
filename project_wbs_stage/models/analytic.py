# Copyright 2017-23 ForgeFlow S.L.
# Copyright 2017-19 Luxim d.o.o.
# Copyright 2017-19 Matmoz d.o.o.
# Copyright 2017-19 Deneroteam.

# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)..

from odoo import SUPERUSER_ID, api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = [("id", "in", stages.ids)]
        stage_ids = stages._search(
            search_domain, order=order, access_rights_uid=SUPERUSER_ID
        )
        return stages.browse(stage_ids)

    stage_id = fields.Many2one(
        "project.project.stage",
        string="Stage",
        ondelete="restrict",
        groups="project.group_project_stages",
        tracking=True,
        index=True,
        copy=False,
        group_expand="_read_group_stage_ids",
    )

    def write(self, values):
        res = super(AccountAnalyticAccount, self).write(values)
        if values.get("stage_id"):
            stage_obj = self.env["base.kanban.stage"]
            for aa in self:
                # Search if there's an associated project
                new_stage = stage_obj.browse(values.get("stage_id"))
                # If the new stage is found in the child accounts, then set
                # it as well (only if the new stage sequence is greater than
                #  the current)
                child_ids = self.search([("parent_id", "=", aa.id)])
                for child in child_ids:
                    if child.stage_id.sequence < new_stage.sequence:
                        child.write({"stage_id": new_stage.id})
            for project in self.project_ids:
                project.write({"stage_id": values.get("stage_id")})
        return res
