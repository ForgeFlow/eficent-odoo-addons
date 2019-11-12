# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Luxim d.o.o.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Deneroteam.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.analytic_resource_plan_stock.tests import (
    test_analytic_resource_plan_stock,
)


class TestAnalyticResourcePlanPurchase(
    test_analytic_resource_plan_stock.TestAnalyticResourcePlanStock
):
    @classmethod
    def setUpClass(cls):
        super(TestAnalyticResourcePlanPurchase, cls).setUpClass()

    def test_res_purchase(self):
        self.assertEqual(
            self.resource_plan_line.qty_available,
            0.0,
            "Showing qty where there is not",
        )
        self.assertEqual(
            self.resource_plan_line.request_state, "none", "should no request"
        )
        self.resource_plan_line.action_button_confirm()
        self.assertEqual(
            self.resource_plan_line.request_state,
            "draft",
            "should draft request",
        )
        purchase_request_line = self.resource_plan_line.purchase_request_lines[
            0
        ]
        purchase_request = purchase_request_line.request_id
        purchase_request.button_to_approve()
        purchase_request.button_approved()
        self.assertEqual(
            self.resource_plan_line.request_state,
            "approved",
            "should approved request",
        )
        self.assertEqual(
            self.resource_plan_line.requested_qty, 1.0, "requested wrong qty"
        )
        self.resource_plan_line.action_button_draft()
        self.assertEqual(
            self.resource_plan_line.request_state,
            "rejected",
            "should rejected request",
        )
