# Copyright 2021 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date, timedelta

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestAnalyticJournalLockDate(TransactionCase):
    def setUp(self):
        super(TestAnalyticJournalLockDate, self).setUp()
        self.analytic_account_model = self.env["account.analytic.account"]
        self.partner_model = self.env["res.partner"]
        self.analytic_line_model = self.env["account.analytic.line"]
        self.analytic_journal_model = self.env["account.analytic.journal"]
        self.analytic_journal = self.analytic_journal_model.create(
            {
                "name": "Labor",
                "code": "LB",
                "type": "general",
                "restrict_lock_dates": True,
            }
        )
        self.unrestricted_analytic_journal = self.analytic_journal_model.create(
            {
                "name": "Labor 2",
                "code": "LB2",
                "type": "general",
                "restrict_lock_dates": False,
            }
        )
        self.analytic_parent1 = self.analytic_account_model.create(
            {"name": "parent aa", "code": "P01"}
        )
        self.analytic_son = self.analytic_account_model.create(
            {
                "name": "son aa",
                "code": "S02",
                "parent_id": self.analytic_parent1.id,
            }
        )
        self.partner_line = self.partner_model.create(
            {
                "name": "Test Partner Line",
            }
        )
        self.analytic_account = self.analytic_account_model.create(
            {
                "name": "Test Analytic Account",
                "surpass_lock_dates": False,
            }
        )
        self.analytic_account_surpass = self.analytic_account_model.create(
            {
                "name": "Test Analytic Account Surpass",
                "surpass_lock_dates": True,
            }
        )

    def test_01_analytic_journal_lock_date(self):
        """
        Test constrains where applicable
        """
        # create future entry --> raise
        with self.assertRaises(ValidationError):
            self.line = self.analytic_line_model.create(
                {
                    "account_id": self.analytic_account.id,
                    "name": "Test Line 1",
                    "date": date.today() + timedelta(days=1),
                    "journal_id": self.analytic_journal.id,
                    "partner_id": self.partner_line.id,
                }
            )
        # create today's entry --> not raise
        self.line = self.analytic_line_model.create(
            {
                "account_id": self.analytic_account.id,
                "name": "Test Line 2",
                "date": date.today(),
                "journal_id": self.analytic_journal.id,
                "partner_id": self.partner_line.id,
            }
        )
        # set custom date and create tomorrow's entry --> not raise
        self.analytic_journal.journal_lock_to_date = date.today() + timedelta(days=2)
        self.line = self.analytic_line_model.create(
            {
                "account_id": self.analytic_account.id,
                "name": "Test Line 3",
                "date": date.today() + timedelta(days=1),
                "journal_id": self.analytic_journal.id,
                "partner_id": self.partner_line.id,
            }
        )
        # remove locking --> not raise
        self.unrestricted_analytic_journal.journal_lock_to_date = (
            date.today() + timedelta(weeks=1)
        )
        self.line = self.analytic_line_model.create(
            {
                "account_id": self.analytic_account.id,
                "name": "Test Line 4",
                "date": date.today() + timedelta(days=1),
                "journal_id": self.unrestricted_analytic_journal.id,
                "partner_id": self.partner_line.id,
            }
        )
        # account is allow to post in the future
        self.analytic_journal.journal_lock_to_date = date.today()
        self.line = self.analytic_line_model.create(
            {
                "account_id": self.analytic_account_surpass.id,
                "name": "Test Line 5",
                "date": date.today() + timedelta(days=1),
                "journal_id": self.analytic_journal.id,
                "partner_id": self.partner_line.id,
            }
        )

    def test_02_hierarchy(self):
        """Test surpass lock dates propagation"""
        self.assertEqual(self.analytic_parent1.surpass_lock_dates, False)
        # changes in the parent affects the son
        self.analytic_parent1.surpass_lock_dates = True
        self.assertEqual(self.analytic_son.surpass_lock_dates, True)
        # changes in the son does not affect the parent
        self.analytic_son.surpass_lock_dates = False
        self.assertEqual(self.analytic_parent1.surpass_lock_dates, True)
