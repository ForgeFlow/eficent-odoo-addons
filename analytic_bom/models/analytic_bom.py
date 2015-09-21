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
from openerp.osv import fields, orm
import time


class AnalyticBom(orm.Model):

    _name = 'analytic.bom'
    _description = "Analytic Bom"

    _columns = {
        'account_id': fields.many2one('account.analytic.account',
                                      'Analytic Account', required=True,
                                      ondelete='cascade', select=True,
                                      domain=[('type', '<>', 'view')],
                                      readonly=True,
                                      states={
                                          'draft': [('readonly', False)]
                                      }),
        'name': fields.related('bom_id', 'name', type='char', readonly=True,
                               string="Bill of Materials name"),
        'date_planned': fields.date('Scheduled Date',
                                    required=True, select=True,
                                    readonly=True,
                                    states={'draft': [('readonly', False)]}),
        'state': fields.selection(
            [('draft', 'Draft'),
             ('confirm', 'Confirmed'),
             ('cancel', 'Cancelled')], 'Status',
            select=True, required=True, readonly=True,
            help=' * The \'Draft\' status is used when a user is encoding '
                 'a new and unconfirmed bom. '
                 '\n* The \'Confirmed\' status is used for to confirm the '
                 'bom line. No further changes are allowed.'
                 '\n* The \'Cancelled\' status is used to cancel '
                 'the bom line.'),
        'product_id': fields.many2one('product.product', 'Product',
                                      readonly=True, required=True,
                                      states={'draft': [('readonly', False)]}),
        'bom_id': fields.many2one('mrp.bom', 'Bill of Materials',
                                  domain=[('bom_id', '=', False)],
                                  readonly=True, required=True,
                                  states={'draft': [('readonly', False)]}),

        'product_uom_id': fields.many2one('product.uom', 'UoM', required=True,
                                          readonly=True,
                                          states={'draft': [('readonly', False)]}),
        'product_qty': fields.float('Quantity', readonly=True, required=True,
                                    states={'draft': [('readonly', False)]},
                                    help='Specifies the amount of '
                                         'quantity to count.'),
    }

    _defaults = {
        'state': 'draft',
        'date_planned': lambda *a: time.strftime('%Y-%m-%d'),
        'product_qty': 1,
    }

    def action_button_draft(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

    def action_button_cancel(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

    def action_button_confirm(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'confirm'}, context=context)

    def on_change_product_id(self, cr, uid, id, product_id, context=None):
        if not product_id:
            return {'value': {
                'product_uom': False,
                'bom_id': False,
            }}
        bom_obj = self.pool.get('mrp.bom')
        product = self.pool.get('product.product').browse(cr, uid, product_id,
                                                          context=context)
        bom_id = bom_obj._bom_find(cr, uid, product.id, product.uom_id and
                                   product.uom_id.id, [])
        product_uom_id = product.uom_id and product.uom_id.id or False
        result = {
            'product_uom_id': product_uom_id,
            'bom_id': bom_id
        }
        return {'value': result}
