# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Luxim d.o.o.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Deneroteam.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestAnalyticSchedule(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestAnalyticSchedule, cls).setUpClass()
        cls.project_project = cls.env["project.project"]
        cls.project = cls.project_project.create(
            {"name": "Test project", "code": "ACV0001"}
        )
        cls.account_id = cls.project.analytic_account_id
        cls.product_simple = cls.env["product.product"].create(
            {"name": "xxx", "type": "product"}
        )
        cls.account_type = cls.env["account.account.type"].create(
            {"name": "Income", "type": "other"}
        )
        cls.general_account_id = cls.env["account.account"].create(
            {
                "name": "Test account",
                "code": "TEST",
                "user_type_id": cls.account_type.id,
            }
        )
        cls.analytic_plan_journal = cls.env[
            "account.analytic.plan.journal"
        ].create(
            {"name": "Sale", "type": "sale", "code": "SAL", "active": True}
        )
        cls.resource_plan_line_simple = cls.env[
            "account.analytic.line.plan"
        ].create(
            {
                "product_id": cls.product_simple.id,
                "product_uom_id": cls.product_simple.uom_id.id,
                "name": "Simple",
                "date": "2020-02-01",
                "account_id": cls.account_id.id,
                "amount": 100000,
                "unit_amount": 1.0,
                "journal_id": cls.analytic_plan_journal.id,
                "general_account_id": cls.general_account_id.id,
            }
        )

    def test_contarct_value(self):
        self.assertEquals(self.account_id.contract_value, 100000.0,
                          "Bad value")
