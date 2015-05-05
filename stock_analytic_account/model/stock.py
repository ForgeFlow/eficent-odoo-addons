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


class stock_move(orm.Model):

    _inherit = "stock.move"

    _columns = {        
        'analytic_account_id': fields.many2one('account.analytic.account',
                                               'Analytic Account'),
        'analytic_account_user_id': fields.related(
            'analytic_account_id', 'user_id', type='many2one',
            relation='res.users', string='Project Manager', store=True,
            readonly=True),
    }


class stock_inventory_line(osv.osv):
    _inherit = "stock.inventory.line"

    _columns = {
        'analytic_account_id': fields.many2one('account.analytic.account',
                                               'Analytic Account'),
    }


class stock_inventory(osv.osv):
    _inherit = "stock.inventory"

    def _inventory_line_hook(self, cr, uid, inventory_line, move_vals):
        """ Creates a stock move from an inventory line
        @param inventory_line:
        @param move_vals:
        @return:
        """
        if inventory_line.analytic_account_id:
            move_vals['analytic_account_id'] = \
                inventory_line.analytic_account_id.id
        return super(stock_inventory, self)._inventory_line_hook(
            cr, uid, inventory_line, move_vals)