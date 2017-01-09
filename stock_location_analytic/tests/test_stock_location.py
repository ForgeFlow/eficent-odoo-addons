# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.osv.orm import except_orm


class TestStockLocation(TransactionCase):

    def setUp(self):
        super(TestStockLocation, self).setUp()
        cr = self.cr
        uid = self.uid
        # Clean up registries
        self.registry('ir.model').clear_caches()
        self.registry('ir.model.data').clear_caches()
        # Get registries
        self.user_model = self.registry("res.users")
        self.location_model = self.registry("stock.location")
        self.analytic_model = self.registry("analytic.account")
        self.move_model= self.registry("stock.move")
        # Get context
        self.context = self.user_model.context_get(self.cr, self.uid)
        context = self.context
        self.yourcompany_loc = self.pool.ref('stock_location_1')
        self.yourcompany_aa = self.pool.ref('analytic_account_1')
        self.AA1 = self.create_analytic(cr, uid, 'AA1', context)
        self.AA2 = self.create_analytic(cr, uid, 'AA2', context)
        self.location1 = self.create_location.create(
            cr, uid, self.AA1, self.yourcompany_loc, context)

    def create_analytic(self, cr, uid, name, context):
        vals = {'name': name,
                'parent_id': self.your_company,
        }
        location_id = self.analytic_model.create(cr, uid, vals, context)
        return location_id


    def create_location(self, cr, uid, analytic, parent, context):
        vals = {'name': analytic.name,
                'location_id': parent,
                'analytic_account_id': analytic.id
        }
        location_id = self.location_model.create(cr, uid, vals, context)
        return location_id

    def test_sublocation_analytic(self, cr, uid, context):
        """Test i cannot create sublocation with different AA"""
        self.assertRaises(except_orm, self.create_location.create(
            cr, uid, self.AA2, self.location1, context))

