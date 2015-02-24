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

    _columns = {
        'analytic_account_id': fields.many2one('account.analytic.account',
                                               'Analytic Account',),
    }

    def action_confirm(self, cr, uid, ids, context=None):
        """ Confirms procurement and writes exception message if any.
        @return: True
        """
        res = super(procurement_order, self).action_confirm(cr, uid,
                                                            ids,
                                                            context=context)
        move_obj = self.pool.get('stock.move')
        for procurement in self.browse(cr, uid, ids, context=context):
            if procurement.analytic_account_id:
                move_obj.write(cr, uid, [procurement.move_id.id],
                               {'analytic_account_id':
                                procurement.analytic_account_id.id},
                               context=context)
        return res