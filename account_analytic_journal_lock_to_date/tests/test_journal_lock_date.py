# -*- coding: utf-8 -*-
# Copyright 2021 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date, timedelta
from odoo.tests import common
from odoo.exceptions import ValidationError


class TestAnalyticJournalLockDate(common.SavepointCase):

    def setUp(cls):
        super(TestAnalyticJournalLockDate, cls).setUp()
        cls.analytic_account_model = cls.env['account.analytic.account']
        cls.partner_model = cls.env["res.partner"]
        cls.analytic_line_model = cls.env['account.analytic.line']
        cls.analytic_journal_model = cls.env["account.analytic.journal"]
        cls.analytic_journal = cls.analytic_journal_model.create(
            {'name': 'Labor',
             'code': 'LB',
             'type': 'general',
             'restrict_lock_dates': True}
        )
        cls.unrestricted_analytic_journal = cls.analytic_journal_model.create(
            {'name': 'Labor 2',
             'code': 'LB2',
             'type': 'general',
             'restrict_lock_dates': False}
        )        
        cls.partner_line = cls.partner_model.create({
            'name': 'Test Partner Line',
        })
        cls.analytic_account = cls.analytic_account_model.create({
            'name': 'Test Analytic Account',
        })

    def test_01_analytic_journal_lock_date(self):
        """
        Test constrains where applicable
        """
        # create future entry --> raise
        with self.assertRaises(ValidationError):
            self.line = self.analytic_line_model.create({
                'account_id': self.analytic_account.id,
                'name': 'Test Line 1',
                'date': date.today() + timedelta(days=1),
                'journal_id': self.analytic_journal.id,
                'partner_id': self.partner_line.id,
            })
        # create todays entry --> not raise
        self.line = self.analytic_line_model.create({
            'account_id': self.analytic_account.id,
            'name': 'Test Line 2',
            'date': date.today(),
            'journal_id': self.analytic_journal.id,
            'partner_id': self.partner_line.id,
        })        
        # set custom date and create tomorrows entry --> not raise
        self.analytic_journal.journal_lock_to_date = date.today() + timedelta(days=2)
        self.line = self.analytic_line_model.create({
            'account_id': self.analytic_account.id,
            'name': 'Test Line 3',
            'date': date.today() + timedelta(days=1),
            'journal_id': self.analytic_journal.id,
            'partner_id': self.partner_line.id,
        })
        # remove locking --> not raise
        self.unrestricted_analytic_journal.journal_lock_to_date = date.today() + timedelta(weeks=1)
        self.line = self.analytic_line_model.create({
            'account_id': self.analytic_account.id,
            'name': 'Test Line 4',
            'date': date.today() + timedelta(days=1),
            'journal_id': self.unrestricted_analytic_journal.id,
            'partner_id': self.partner_line.id,
        })
