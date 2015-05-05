# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent (<http://www.eficent.com/>)
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
from openerp.osv import fields, osv, orm
import openerp.addons.decimal_precision as dp


class account_analytic_account(orm.Model):

    _inherit = "account.analytic.account"

    def _get_stock(self, cr, uid, ids, field_name, arg, context=None):
        """ Gets stock of products for locations
        @return: Dictionary of values
        """
        if context is None:
            context = {}
        if 'location_id' not in context:
            locations = self.pool.get('stock.location').search(
                cr, uid, [('usage', '=', 'internal')], context=context)
        else:
            locations = context['location_id'] \
                and [context['location_id']] or []

        if isinstance(ids, (int, long)):
            ids = [ids]

        res = {}.fromkeys(ids, 0.0)
        if locations:
            cr.execute('''select
                    analytic_account_id,
                    sum(qty)
                from
                    stock_report_analytic_account
                where
                    location_id IN %s and analytic_account_id
                    IN %s group by analytic_account_id''',
                       (tuple(locations), tuple(ids),))
            res.update(dict(cr.fetchall()))

        return res

    def _stock_search(self, cr, uid, obj, name, args, context=None):
        """ Searches Ids of products
        @return: Ids of locations
        """
        locations = self.pool.get('stock.location').search(
            cr, uid, [('usage', '=', 'internal')])
        cr.execute('''select
                analytic_account_id,
                sum(qty)
            from
                stock_report_analytic_account
            where
                location_id IN %s group by analytic_account_id
            having  sum(qty) ''' + str(args[0][1]) + str(args[0][2]),
                   (tuple(locations),))
        res = cr.fetchall()
        ids = [('id', 'in', map(lambda x: x[0], res))]
        return ids

    _columns = {
        'stock_available': fields.function(
            _get_stock, fnct_search=_stock_search, type="float",
            string="Available", select=True,
            help="Current quantity of products with this Analytic Account in "
                 "company warehouses",
            digits_compute=dp.get_precision('Product Unit of Measure')),
        'move_ids': fields.one2many('stock.move', 'analytic_account_id',
                                    'Moves for this analytic account',
                                    readonly=True),
    }
