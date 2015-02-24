# -*- coding: utf-8 -*-
##############################################################################
#
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
from openerp.osv import orm, fields


class procurement_order(orm.Model):
    _inherit = "procurement.order"

    def create_procurement_purchase_order(self, cr, uid, procurement, po_vals, line_vals, context=None):
        """Create the purchase order from the procurement, using
           the provided field values, after adding the given purchase
           order line in the purchase order.

           :params procurement: the procurement object generating the purchase order
           :params dict po_vals: field values for the new purchase order (the
                                 ``order_line`` field will be overwritten with one
                                 single line, as passed in ``line_vals``).
           :params dict line_vals: field values of the single purchase order line that
                                   the purchase order will contain.
           :return: id of the newly created purchase order
           :rtype: int
        """
        if procurement.analytic_account_id:
            line_vals.update({
                'account_analytic_id': procurement.analytic_account_id.id
            })
        return super(procurement_order, self).\
            create_procurement_purchase_order(cr, uid, procurement, po_vals,
                                              line_vals, context=context)
