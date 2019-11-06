# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestAccountAnalyticPost(common.TransactionCase):
    def setUp(self):
        super(TestAccountAnalyticPost, self).setUp()
        self.move_obj = self.env["account.move"]
        self.move_line_obj = self.env["account.move.line"]
        self.analytic_account_obj = self.env["account.analytic.account"]
        self.account_obj = self.env["account.account"]
        self.journal_obj = self.env["account.journal"]
        self.users_obj = self.env["res.users"]
        self.company_id = self.users_obj.browse(self.env.uid).company_id.id
        self.account_cash = self.account_obj.search(
            [("user_type_id.type", "=", "liquidity")], limit=1
        )
        self.account_Income = self.account_obj.search(
            [("user_type_id.name", "=", "Income")], limit=1
        )
        self.journal_obj.create({
            "name": "something",
            "type": "sale",
            "code": "prefix",
            "company_id": self.company_id,
        })
        self.journal = self.journal_obj.search(
            [("type", "=", "sale")], limit=1
        )
        self.analytic_account_id = self.analytic_account_obj.create(
            {"name": "Test Analytic Account "}
        )

    def _create_move(self):
        self.move = self.move_obj.create(
            {
                "name": "/",
                "ref": "2011010",
                "journal_id": self.journal.id,
                "state": "draft",
                "company_id": self.company_id,
            }
        )
        self.move_line_obj.create(
            {
                "account_id": self.account_cash.id,
                "name": "Basic Computer 1",
                "move_id": self.move.id,
                "analytic_account_id": self.analytic_account_id.id,
            }
        )
        self.move_line_obj.create(
            {
                "account_id": self.account_Income.id,
                "name": "Basic Computer 2",
                "move_id": self.move.id,
                "analytic_account_id": self.analytic_account_id.id,
            }
        )
        self.move_line_obj.create(
            {
                "account_id": self.account_Income.id,
                "name": "Basic Computer 3",
                "move_id": self.move.id,
                "analytic_account_id": self.analytic_account_id.id,
            }
        )
        return self.move

    def test_create_analytic_lines(self):
        move_id = self._create_move()
        move_id.post()
        valid_to_post_id = self.move_line_obj.search(
            [
                ("id", "in", move_id.line_ids.ids),
                ("account_id.user_type_id.name", "in", ["Income", "Expenses"]),
            ]
        )
        self.assertEqual(len(valid_to_post_id), 2)
