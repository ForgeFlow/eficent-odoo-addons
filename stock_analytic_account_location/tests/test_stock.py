# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestStock(TransactionCase):

    def setUp(self):
        super(TestStock, self).setUp()
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
        self.location1 = self.create_location.create(
            cr, uid, self.AA1, self.yourcompany_loc, 'internal', self.context)
        self.location2 = self.create_location.create(
            cr, uid, self.AA1, self.yourcompany_loc, 'customer', self.context)
        self.location3 = self.create_location.create(
            cr, uid, None, self.yourcompany_loc, 'internal', self.context)
        self.location4 = self.create_location.create(
            cr, uid, None, self.yourcompany_loc, 'customer', self.context)
        self.usb_adapter_id = self.ir_model_data.get_object_reference(
            self.cr, self.uid, 'product', 'product_product_48')[1]
        self.unit_id = self.ir_model_data.get_object_reference(
            self.cr, self.uid, 'product', 'product_uom_unit')[1]
        self.move1 = self.create_move(cr, uid, 'out_aa', self.location1,
                                      self.location4, self.context)
        self.move2 = self.create_move(cr, uid, 'out', self.location3,
                                      self.location4, self.context)
        self.move3 = self.create_move(cr, uid, 'in_aa', self.location4,
                                      self.location1, self.context)
        self.move4 = self.create_move(cr, uid, 'in', self.location4,
                                      self.location3, self.context)


    def create_analytic(self, cr, uid, name, context):
            vals = {'name': name,
                    'parent_id': self.your_company,
            }
            location_id = self.analytic_model.create(cr, uid, vals, context)
            return location_id


    def create_location(self, cr, uid, analytic, parent, usage, context):
        vals = {'name': analytic.name,
                'location_id': parent,
                'usage': usage,
                'analytic_account_id': analytic.id
        }
        location_id = self.location_model.create(cr, uid, vals, context)
        return location_id

    def create_move(self, cr, uid, name, src, dest, context):
        vals = {
            'name': name,
            'product_id': self.usb_adapter_id,
            'product_qty': 1.0,
            'product_uom': self.unit_id,
            'location_id': src,
            'location_dest_id': dest,
        }
        move = self.move_model.create(cr, uid, vals, context)
        self.move_model.action_done(cr, uid, move, context)
        return move

    def test_move_anaytic(self):
        """Test move have or not analytic account"""
        self.assertEqual(self.move1.analytic_account_id.id, self.AA1)
        self.assertEqual(self.move2.analytic_account_id.id, None)
        self.assertEqual(self.move3.analytic_account_id.id, self.AA1)
        self.assertEqual(self.move4.analytic_account_id.id, None)
