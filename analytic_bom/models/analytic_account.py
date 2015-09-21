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


class AccountAnalyticAccount(orm.Model):

    _inherit = "account.analytic.account"

    _columns = {
        'analytic_bom_ids': fields.one2many('analytic.bom',
                                            'account_id',
                                            'BOMs for this analytic '
                                            'account',
                                            readonly=True),
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}
        default['analytic_bom_ids'] = []
        res = super(AccountAnalyticAccount, self).copy(cr, uid, id, default,
                                                       context)
        return res
