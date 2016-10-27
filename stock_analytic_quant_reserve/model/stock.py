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
from openerp.tools.translate import _
import logging
from openerp import netsvc
from openerp.tools import float_compare

_logger = logging.getLogger(__name__)


class StockMove(orm.Model):

    _inherit = "stock.move"

    _columns = {
        'analytic_reserved': fields.boolean(
            'Reserved',
            help="Reserved for the Analytic Account"
        ),
    }

    def _get_analytic_reserved(self, cr, uid, vals, context=None):
        context = context or {}
        analytic_obj = self.pool['account.analytic.account']
        aaid = vals['account_analytic_id']
        if aaid:
            aa = analytic_obj.browse(cr, uid, aaid, context=context)
            return aa.use_reserved_stock
        else:
            return False

    def create(self, cr, uid, vals, context=None):
        if 'account_analytic_id' in vals:
            vals['analytic_reserved'] = self._get_analytic_reserved(
                cr, uid, vals, context=context)
        return super(StockMove, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if 'account_analytic_id' in vals:
            vals['analytic_reserved'] = self._get_analytic_reserved(
                cr, uid, vals, context=context)
        return super(StockMove, self).write(cr, uid, ids, vals,
                                            context=context)


class StockQuant(orm.Model):
    _inherit = "stock.quant"

    def quants_reserve(self, cr, uid, quants, move, link=False, context=None):
        '''If the quant is related to an analytic account other projects
        cannot create moves
        '''
        quants2 = []
        req_analytic_account = move.account_analytic_id
        for quant in quants:
            if quant[0]:
                if req_analytic_account:
                    if quant[0].analytic_account_id and quant[0].\
                            analytic_account_id != req_analytic_account:
                        continue
                quants2.append(quant)

        # Filter the quants if move has an analytic account
        #quants_2 = filtered(quants)
        return super(StockQuant, self).quants_reserve(cr, uid, quants2,
                                                      move, link, context)
