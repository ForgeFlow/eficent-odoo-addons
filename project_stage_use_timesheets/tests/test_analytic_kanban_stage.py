# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from odoo.tests import common


class TestAnalyticKanban(common.TransactionCase):
    def setUp(self):
        super(TestAnalyticKanban, self).setUp()

        self.analytic_obj = self.env["account.analytic.account"]
        self.project_obj = self.env["project.project"]
        self.partner_obj = self.env["res.partner"]
        self.kanban_stage_model = self.env["base.kanban.stage"]

        # Create partners
        customer1 = self.partner_obj.create({"name": "Customer 1"})
        # Create analytic group and operation:
        self.project_ts = self.project_obj.create(
            {
                "partner_id": customer1.id,
                "name": "TS",
                "account_class": "work_package",
            }
        )
        self.analytic_ts = self.project_ts.analytic_account_id
        self.stage_ts = self.kanban_stage_model.create(
            {
                "name": "TS",
                "allow_timesheets": True,
                "res_model_id": self.env.ref(
                    "analytic.model_account_analytic_account"
                ).id,
            }
        )
        self.stage_no_ts = self.kanban_stage_model.create(
            {
                "name": "NO TS",
                "allow_timesheets": False,
                "res_model_id": self.env.ref(
                    "analytic.model_account_analytic_account"
                ).id,
            }
        )

    def test_read_group_stage_ids(self):
        self.analytic_ts.stage_id = self.stage_ts
        self.assertEqual(self.analytic_ts.project_ids.allow_timesheets, True)
        self.analytic_ts.stage_id = self.stage_no_ts
        self.assertEqual(self.analytic_ts.project_ids.allow_timesheets, False)
