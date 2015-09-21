# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent (<http://www.eficent.com/>)
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
from openerp.tools.translate import _


class PurchaseRequisition(orm.Model):
    _inherit = "purchase.requisition"

    def make_purchase_order(self, cr, uid, ids, partner_id, context=None):

        if context is None:
            context = {}

        for requisition in self.browse(cr, uid, ids, context=context):
            for line in requisition.line_ids:
                if not line.product_id and (line.manufacturer_pref or
                                            line.manufacturer_pname or
                                            line.manufacturer):
                    raise orm.except_orm(
                        _('Error!'),
                        _('All items with a manufacturer product code '
                          'or name, must have a corresponding product assigned'
                          ''))
        return super(PurchaseRequisition, self).make_purchase_order(
            cr, uid, ids, partner_id, context=context)
