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

    def make_po(self, cr, uid, ids, context=None):
        res = super(procurement_order, self).make_po(cr, uid, ids,
                                                     context=context)
        requisition_line_obj = self.pool.get('purchase.requisition.line')
        for procurement in self.browse(cr, uid, ids, context=context):
            if procurement.analytic_account_id and procurement.requisition_id:
                for line_id in procurement.requisition_id.line_ids:
                    requisition_line_obj.write(
                        cr, uid, [line_id.id], {
                            'account_analytic_id':
                                procurement.analytic_account_id.id})

        return res