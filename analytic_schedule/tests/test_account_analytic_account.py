# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase
import time


class TestAccountAnalyticAccount(TransactionCase):

    def setUp(self):
        super(TestAccountAnalyticAccount, self).setUp()
        self.analytic_account_obj = self.env['account.analytic.account']
        self.analytic_line_obj = self.env['account.analytic.line']
        self.partner1 = self.env.ref('base.res_partner_1')
        self.partner2 = self.env.ref('base.res_partner_2')
        self.analytic_parent = self.analytic_account_obj.create({
            'name': 'Test Parent',
            'code': '01',
        })
        self.analytic_son = self.analytic_account_obj.create({
            'name': 'Test First Son',
            'code': '02',
            'parent_id': self.analytic_parent.id,
            'date_start': time.strftime('%Y-%m-21'),
            'date': time.strftime('%Y-%m-20'),
        })
        self.analytic_son_1 = self.analytic_account_obj.create({
            'name': 'Test Second Son ',
            'code': '02',
            'parent_id': self.analytic_parent.id,
            'date_start': time.strftime('%Y-%m-11'),
            'date': time.strftime('%Y-%m-10'),
        })

    def test_methods(self):
        self.assertEqual(self.analytic_parent.date_start,
                         self.analytic_son_1.date_start)
        self.assertEqual(self.analytic_parent.date,
                         self.analytic_son.date)
