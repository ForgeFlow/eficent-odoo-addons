# Copyright 2015 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields
from odoo.tests import Form, common


class TestAnalyticWipReport(common.TransactionCase):
    def setUp(self):
        super(TestAnalyticWipReport, self).setUp()
        self.AnalyticAccountObject = self.env["account.analytic.account"]
        self.account_model = self.env["account.account"]

        self.partner = self.env.ref("base.res_partner_2")
        self.receivable = self.env.ref("account.data_account_type_receivable")
        self.analytic_plan_version = self.env.ref(
            "analytic_plan.analytic_plan_version_P02"
        )

        self.account = self.AnalyticAccountObject.create(
            {"name": "AnalyticAccount Parent for Test", "partner_id": self.partner.id}
        )

    def test_check_wip_report(self):
        self.invoice_account = self.account_model.search(
            [("user_type_id", "=", self.receivable.id)], limit=1
        )
        move_form = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        move_form.invoice_date = fields.Date.from_string("2019-01-01")
        move_form.date = move_form.invoice_date
        move_form.partner_id = self.partner

        with move_form.invoice_line_ids.new() as line_form:
            line_form.name = "Test invoice line"
            line_form.account_id = self.invoice_account
            line_form.quantity = 2
            line_form.price_unit = 100
            line_form.analytic_account_id = self.account

        self.invoice = move_form.save()

        self.invoice._post()
        self.account._compute_wip_report()
        self.assertEqual(self.account.earned_revenue, 0)
        self.assertEqual(self.account.total_value, 0)
        self.assertEqual(self.account.actual_costs, 0)
        self.assertEqual(self.account.total_estimated_costs, 0)
