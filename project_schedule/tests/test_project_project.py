# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase
import time


class TestProjectProject(TransactionCase):

    def setUp(self):
        super(TestProjectProject, self).setUp()
        self.project_obj = self.env['project.project']
        self.partner1 = self.env.ref('base.res_partner_1')
        self.partner2 = self.env.ref('base.res_partner_2')
        self.project_parent = self.project_obj.create({
            'name': 'Test Parent',
            'code': '01',
        })
        self.project_son = self.project_obj.create({
            'name': 'Test First Son',
            'code': '02',
            'parent_id': self.project_parent.id,
            'date_start': time.strftime('%Y-%m-21'),
            'date': time.strftime('%Y-%m-20'),
        })
        self.project_son_1 = self.project_obj.create({
            'name': 'Test Second Son ',
            'code': '02',
            'parent_id': self.project_parent.id,
            'date_start': time.strftime('%Y-%m-11'),
            'date': time.strftime('%Y-%m-10'),
        })

    def test_methods(self):
        self.assertEqual(self.project_parent.date_start,
                         self.project_son_1.date_start)
        self.assertEqual(self.project_parent.date,
                         self.project_son.date)
