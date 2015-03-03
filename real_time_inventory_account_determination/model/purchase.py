# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
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

from openerp.osv import fields, orm
from openerp.tools.translate import _


class purchase_order(orm.Model):
    _inherit = "purchase.order"

    def _choose_account_from_po_line(self, cr, uid, order_line, context=None):
        account_id = super(purchase_order, self)._choose_account_from_po_line(
            cr, uid, order_line, context=context)
        if (
            order_line.product_id
            and order_line.product_id.type != 'service'
            and order_line.product_id.valuation == 'real_time'
        ):
            # Only consider if it's going to be moved to a company location
            if order_line.order_id.location_id \
                    and order_line.order_id.location_id.company_id:
                acc_id = \
                    order_line.product_id.property_stock_account_input \
                    and order_line.product_id.property_stock_account_input.id
                if not acc_id:
                    acc_id = order_line.product_id.categ_id.\
                        property_stock_account_input_categ \
                        and order_line.product_id.categ_id.\
                        property_stock_account_input_categ.id
                if acc_id:
                    fpos = order_line.order_id.fiscal_position or False
                    account_id = self.pool.get('account.fiscal.position').\
                        map_account(cr, uid, fpos, acc_id)
        return account_id

    def wkf_confirm_order(self, cr, uid, ids, context=None):
        for po in self.browse(cr, uid, ids, context=context):
            for line in po.order_line:
                if (
                    line.product_id.valuation == 'real_time'
                    and line.product_id.type != 'service'
                    and not po.dest_address_id
                    and po.invoice_method in ('manual', 'order')
                ):
                    raise orm.except_orm(
                        _('Error!'),
                        _('It is not possible to confirm a purchase order '
                          'with invoice control method "Based on generated '
                          'draft invoice" or "Based on Purchase Order lines". '
                          'if the PO contains at least one line with a '
                          'non-service product set with real time inventory '
                          'valuation, and the the PO is not being directly '
                          'shipped to a third party.'))
        return super(purchase_order, self).wkf_confirm_order(cr, uid, ids,
                                                             context=None)