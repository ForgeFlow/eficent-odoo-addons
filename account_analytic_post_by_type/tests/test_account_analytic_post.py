# -*- coding: utf-8 -*-
# © 2016 - Eficent http://www.eficent.com/
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from openerp.tests import common
from openerp.osv import orm


class test_account_analytic_post(common.TransactionCase):

    def setUp(self):
        super(test_account_analytic_post, self).setUp()
        self.account_obj = self.env['account.account']
        self.account_type_obj = self.env['account.account.type']
        self.move_obj = self.env['account.move']
        self.move_line_obj = self.env['account.move.line']
        self.analytic_account_obj = self.env['account.analytic.account']
        self.analytic_line_obj = self.env['account.analytic.line']
        self.analytic_account_id = self.analytic_account_obj.create(
            {'name': 'test aa', 'type': 'normal'})

    def _create_move(self, with_analytic, amount=100):
        date = datetime.now()
        period_id = self.env['account.period'].find(
            date,
            context={'account_period_prefer_normal': True})[0]
        move_vals = {
            'journal_id': self.ref('account.sales_journal'),
            'period_id': period_id.id,
            'date': date,
        }
        move_id = self.move_obj.create(move_vals)
        self.move_line_obj.create(
            {'move_id': move_id.id,
             'name': '/',
             'debit': 0,
             'credit': amount,
             'account_id': self.ref('account.a_sale'),
             'analytic_account_id':
             self.analytic_account_id if with_analytic else False})
        self.move_line_obj.create(
            {'move_id': move_id.id,
             'name': '/',
             'debit': amount,
             'credit': 0,
             'account_id': self.ref('account.a_recv')})
        return move_id

    def test_no_analytic(self):
        move = self._create_move(with_analytic=False)
        move.button_validate()
        entry = self.move_line_obj.search([('move_id','=',move.id)])
        self.assertEqual(len(entry), 1, "No analytic entries not"
                                              " affected")

    def test_no_post(self):
        move = self._create_move(with_analytic=False)
        move.button_validate()
        entry = self.move_line_obj.search([('move_id', '=', move.id)])
        self.assertEqual(len(entry), 0, "No profit & loss associated")

    def test_post(self):
        move = self._create_move(with_analytic=False)
        move.button_validate()
        entry = self.move_line_obj.search([('move_id', '=', move.id)])
        self.assertEqual(len(entry), 1, "Post as is a profit and loss "
                                              "account")
