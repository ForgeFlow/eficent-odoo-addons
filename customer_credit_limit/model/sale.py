# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Sistemas Adhoc
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _


class sale_order(osv.osv):
    _inherit = "sale.order"

    def check_limit(self, cr, uid, ids, context=None):

        model_data_obj = self.pool.get('ir.model.data')
        res_groups_obj = self.pool.get('res.groups')
        currency_obj = self.pool.get('res.currency')

        for order in self.browse(cr, uid, ids, context=context):
            if order.order_policy == 'prepaid':
                continue
            partner = order.partner_id
            group_releaser_id = model_data_obj._get_id(
                cr, uid, 'customer_credit_limit',
                'group_so_credit_block_releaser')
            if group_releaser_id:
                res_id = model_data_obj.read(cr, uid, [group_releaser_id],
                                             ['res_id'])[0]['res_id']
                group_releaser = res_groups_obj.browse(
                    cr, uid, res_id, context=context)
                group_user_ids = [user.id for user
                                  in group_releaser.users]

                if order.currency_id.id != \
                        order.company_id.currency_id.id:
                    so_total_cc = currency_obj.compute(
                        cr, uid, order.currency_id.id,
                        order.company_id.currency_id.id,
                        order.amount_total, context=context)
                    total_order_amount = so_total_cc
                else:
                    total_order_amount = \
                        order.amount_total
                available_credit = partner.credit_limit \
                    - partner.total_credit_exposure - total_order_amount

                if available_credit < 0 and uid not in group_user_ids:
                    raise osv.except_osv(
                        _('Credit exceeded'),
                        _('Cannot confirm the order. The credit '
                          'limit would be exceeded by %s %s. '
                          'You can still process the Sales Order '
                          'by changing the Invoice Policy to '
                          '"Before Delivery."')
                        % (abs(available_credit),
                           order.company_id.currency_id.name))

        return True
