# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from openerp import tools


class StockChangeAnalyticAccount(orm.TransientModel):
    _inherit = "stock.change.analytic.account"

    _columns = {
        'src_analytic_account_id': fields.many2one(
            'account.analytic.account', 'Source Analytic Account'),
        'dest_analytic_account_id': fields.many2one(
            'account.analytic.account', 'Source Analytic Account'),
        'location_id': fields.many2one(
            'stock.location', 'Source Location', readonly=True, required=True),
        'location_dest_id': fields.many2one(
                'stock.location', 'Destination Location', readonly=True,
                required=True),
        'quantity': fields.float('Quantity'),
    }

    def default_get(self, cr, uid, fields, context=None):
        res = super(StockChangeAnalyticAccount,
                    self).default_get(cr, uid, fields, context=context)
        product_obj = self.pool['product.product']
        product_ids = context.get('active_ids', [])
        active_model = context.get('active_model')

        if not product_ids:
            return res
        assert active_model == 'product.product', \
            'Bad context propagation'

        items = []
        for line in product_obj.browse(cr, uid, request_line_ids,
                                            context=context):
                items += self._prepare_item(cr, uid, line, context=context)
        res['item_ids'] = items

        return res