# -*- coding: utf-8 -*-
# © 2015 Akretion, Benoît GUILLOT
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp import netsvc
import time


class TestInvoice(TransactionCase):

    def setUp(self):
        super(TestInvoice, self).setUp()
        cr, uid, context = self.cr, self.uid, {}
        data_model = self.registry('ir.model.data')
        self.partner_model = self.registry('res.partner')
        self.res_users_model = self.registry('res.users')
        self.invoice_model = self.registry('account.invoice')
        self.currency_model = self.registry('res.currency')
        self.currency_rate_model = self.registry('res.currency.rate')
        self.res_company_model = self.registry('res.company')
        self.product_model = self.registry('product.product')
        self.inv_line_model = self.registry('account.invoice.line')
        self.company_model = self.registry('res.company')
        # company
        self.company = data_model.get_object(cr, uid, 'base', 'main_company')
        self.grp_acc_user = data_model.get_object(cr, uid, 'account',
                                                  'group_account_invoice')
        # Partner
        self.partner1 = data_model.get_object(cr, uid, 'base',
                                              'res_partner_1')

        # Products
        self.product1 = data_model.get_object(cr, uid, 'product',
                                              'product_product_7')

        # Create user1
        self.user1_id = self._create_user(cr, uid, 'user_1',
                                          [self.grp_acc_user],
                                          self.company, context=context)

        # Create currency
        self.currency_id = self._create_currency(cr, uid,
                                                 self.company,
                                                 context=context)

        # Create & validate an invoice
        self.invoice_id = self._create_validate_invoice(
                cr, self.user1_id, [(self.product1, 1000)], self.currency_id,
                context=context)

    def _create_user(self, cr, uid, login, groups, company, context=None):
        """Create a user."""
        group_ids = [group.id for group in groups]
        user_id = self.res_users_model.create(cr, uid, {
            'name': 'Test Account User',
            'login': login,
            'password': 'demo',
            'email': 'example@yourcompany.com',
            'company_id': company.id,
            'company_ids': [(4, company.id)],
            'groups_id': [(6, 0, group_ids)]
        })
        return user_id

    def _create_currency(self, cr, uid, company, context=None):
        """Create a user."""
        currency_id = self.currency_model.create(cr, uid, {
            'name': 'TST',
            'company_id': company.id,
        })
        self.currency_rate_model.create(cr, uid, {
            'currency_id': currency_id,
            'rate': 0.6,
            'name': time.strftime('%Y-%m-%d 00:00:00'),
        })
        return currency_id


    def _create_validate_invoice(self, cr, uid, line_products,
                                 currency_id, context=None):
        """Create invoice.
        ``line_products`` is a list of tuple [(product, qty)]
        """
        part_id = self.partner1.id
        # Call partner onchange
        inv_vals = self.invoice_model.onchange_partner_id(cr, uid, [],
                                                          'in_invoice',
                                                          part_id)['value']
        # Get default values of invoice
        default_inv_vals = self.invoice_model.default_get(cr, uid, [])
        inv_vals.update(default_inv_vals)
        lines = []
        # Prepare invoice lines
        for product, qty in line_products:
            uom_id = product.uom_id.id
            line_values = {
                'product_id': product.id,
                'quantity': qty,
            }
            # Call product onchange
            line_res = self.inv_line_model.product_id_change(
                    cr, uid, [], product.id, uom_id, qty, type='in_invoice',
                    currency_id=currency_id, partner_id=part_id)['value']
            line_values.update(line_res)
            line_values.update({'price_unit': 50}),
            lines.append((0, 0, line_values))
        inv_vals.update({
            'partner_id': self.partner1.id,
            'account_id': self.partner1.property_account_payable.id,
            'invoice_line': lines,
            'currency_id': currency_id,
        })

        # Create invoice
        invoice_id = self.invoice_model.create(cr, uid, inv_vals)
        self.invoice = self.invoice_model.browse(cr, self.user1_id, invoice_id,
                                                 context=context)
        # Force exchange rate
        self.invoice_force_currency_rate_model = \
            self.registry['invoice.force.currency.rate']
        rate = 0.5
        self.invoice_force_currency_rate_id = \
            self.invoice_force_currency_rate_model.create(
                    cr, uid, {'currency_rate': rate})
        self.invoice_force_currency_rate_model.force_currency_rate(
                cr, uid, [self.invoice_force_currency_rate_id], {
                    'lang': 'en_US',
                    'active_model': 'account.invoice',
                    'active_ids': [invoice_id],
                    'tz': False,
                    'active_id': invoice_id
                })

        # Validate the invoice
        self.invoice.signal_workflow('invoice_open')

        return invoice_id

    def test_account_moves(self):
        """
        Check if journal entries of the invoice have the correct exchange rate
        """
        for line in self.invoice.move_id.line_id:
            if line.account_id == self.invoice.account_id:
                expected_val = 1000 * 50 * 0.5
                self.assertEquals(line.debit, expected_val)
                break
