# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestAnalyticWipReportExtend(common.TransactionCase):
    def setUp(self):
        super(TestAnalyticWipReportExtend, self).setUp()
        self.AnalyticAccountObject = self.env["account.analytic.account"]
        self.account_invoice = self.env["account.invoice"]
        self.account_model = self.env["account.account"]

        self.partner = self.env.ref("base.res_partner_2")
        self.receivable = self.env.ref("account.data_account_type_receivable")
        self.analytic_plan_version = self.env.ref(
            "analytic_plan.analytic_plan_version_P02"
        )

        self.account = self.AnalyticAccountObject.create(
            {
                "name": "AnalyticAccount Parent for Test",
                "partner_id": self.partner.id,
            }
        )

    def test_check_wip_report(self):
        self.invoice_account = self.account_model.search(
            [("user_type_id", "=", self.receivable.id)], limit=1
        )
        self.invoice = self.account_invoice.create(
            {
                "partner_id": self.partner.id,
                "type": "out_invoice",
                "account_id": self.invoice_account.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Test invoice line",
                            "account_id": self.invoice_account.id,
                            "quantity": 2,
                            "price_unit": 100,
                            "account_analytic_id": self.account.id,
                        },
                    )
                ],
            }
        )
        self.invoice.action_invoice_open()
        self.account._compute_wip_report()
        self.assertEquals(self.account.estimated_gross_profit_per, 0)
        self.assertEquals(self.account.under_over, 0)
