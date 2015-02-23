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

from openerp.osv import fields, orm


class mrp_production(orm.Model):
    _inherit = 'mrp.production'

    _columns = {
        'analytic_account_id': fields.many2one('account.analytic.account',
                                               'Analytic Account',),
    }

    def _hook_create_post_procurement(self, cr, uid, production,
                                      procurement_id, context=None):
        res = super(mrp_production, self)._hook_create_post_procurement(
            cr, uid, production, procurement_id, context=context)
        procurement_order = self.pool.get('procurement.order')
        if production.analytic_account_id:
            procurement_order.write(cr, uid, [procurement_id], {
                'analytic_account_id': production.analytic_account_id.id})
        return res

    def _make_production_produce_line(self, cr, uid, production, context=None):
        stock_move = self.pool.get('stock.move')
        move_id = super(mrp_production, self)._make_production_produce_line(
            cr, uid, production, context=context)
        if production.analytic_account_id:
            stock_move.write(cr, uid, [move_id], {
                'analytic_account_id': production.analytic_account_id.id
            }, context=context)
        return move_id

    def _make_production_consume_line(self, cr, uid, production_line,
                                      parent_move_id,
                                      source_location_id=False,
                                      context=None):
        stock_move = self.pool.get('stock.move')
        move_id = super(mrp_production, self)._make_production_consume_line(
            cr, uid, production_line, parent_move_id,
            source_location_id=source_location_id, context=context)
        production = production_line.production_id
        if production.analytic_account_id:
            stock_move.write(cr, uid, [move_id], {
                'analytic_account_id': production.analytic_account_id.id
            }, context=context)
        return move_id

    def _costs_generate(self, cr, uid, production):
        """ Calculates total costs at the end of the production.
        Records the cost in the analytic account associated to
        the manufacturing order.
        Considers only machine (material costs). Human costs
        will be taken into account by means of module
        mrp_workorder_line_work.
        @param production: Id of production order.
        @return: Calculated amount.
        """
        super(mrp_production, self)._costs_generate(cr, uid, production)
        amount = 0.0
        analytic_line_obj = self.pool.get('account.analytic.line')
        for wc_line in production.workcenter_lines:
            wc = wc_line.workcenter_id
            if wc.costs_journal_id and wc.costs_general_account_id \
                    and wc.resource_type == 'material':
                # Cost per hour
                value = wc_line.hour * wc.costs_hour
                account = production.analytic_account_id.id
                if value and account:
                    amount += value
                    analytic_line_obj.create(cr, uid, {
                        'name': wc_line.name + ' (H)',
                        'amount': value,
                        'account_id': account,
                        'general_account_id': wc.costs_general_account_id.id,
                        'journal_id': wc.costs_journal_id.id,
                        'ref': wc.code,
                        'product_id': wc.product_id.id,
                        'unit_amount': wc_line.hour,
                        'product_uom_id': wc.product_id
                        and wc.product_id.uom_id.id or False
                    })
                # Cost per cycle
                value = wc_line.cycle * wc.costs_cycle
                account = production.analytic_account_id.id
                if value and account:
                    amount += value
                    analytic_line_obj.create(cr, uid, {
                        'name': wc_line.name+' (C)',
                        'amount': value,
                        'account_id': account,
                        'general_account_id': wc.costs_general_account_id.id,
                        'journal_id': wc.costs_journal_id.id,
                        'ref': wc.code,
                        'product_id': wc.product_id.id,
                        'unit_amount': wc_line.cycle,
                        'product_uom_id': wc.product_id
                        and wc.product_id.uom_id.id or False
                    })
        return amount