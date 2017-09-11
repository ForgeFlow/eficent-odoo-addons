# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase
from odoo import fields


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
            'name': 'Test Son',
            'code': '02',
            'parent_id': self.analytic_parent.id,
            'date_start': fields.Date.today(),
            'date': fields.Date.today(),
        })
        self.analytic_parent.write({'partner_id': self.partner1.id})
        self.analytic_son.write({'partner_id': self.partner2.id})

    def test_methods(self):
        self.assertEqual(self.analytic_parent.date_start,
                         self.analytic_son.date_start)
        self.assertEqual(self.analytic_parent.date,
                         self.analytic_son.date)
