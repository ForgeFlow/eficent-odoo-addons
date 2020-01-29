from odoo.tests import common
from odoo.exceptions import UserError


class TestMrpAnalyticLocation(common.TransactionCase):
    def setUp(self):
        super(TestMrpAnalyticLocation, self).setUp()
        self.location = self.env["stock.location"].create(
            {"name": "AA loc", "usage": "internal", "company_id": False}
        )
        self.analytic_account = self.env["account.analytic.account"].create(
            {"name": "Analytic account test", "location_id": self.location.id}
        )
        self.analytic_account2 = self.env["account.analytic.account"].create(
            {"name": "Analytic account test"}
        )
        self.location.analytic_account_id = self.analytic_account.id
        self.product = self.env["product.product"].create(
            {"name": "Test product"}
        )
        self.bom = self.env["mrp.bom"].create(
            {
                "product_id": self.product.id,
                "product_tmpl_id": self.product.product_tmpl_id.id,
            }
        )
        self.production = self.env["mrp.production"].create(
            {
                "product_id": self.product.id,
                "analytic_account_id": self.analytic_account.id,
                "product_uom_id": self.product.uom_id.id,
                "bom_id": self.bom.id,
            }
        )

    def test_loc_productions(self):
        self.assertEqual(
            self.analytic_account.location_id, self.production.location_src_id
        )

    def test_no_loc(self):
        with self.assertRaises(UserError):
            self.production = self.env["mrp.production"].create(
                {
                    "product_id": self.product.id,
                    "analytic_account_id": self.analytic_account2.id,
                    "product_uom_id": self.product.uom_id.id,
                    "bom_id": self.bom.id,
                }
            )
            self.production.onchange_analytic()
