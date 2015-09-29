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
import openerp.addons.decimal_precision as dp


class StockPicking(orm.Model):

    _inherit = 'stock.picking'

    _columns = {
        'weight_uom_id': fields.many2one(
            'product.uom', 'Unit of Measure', required=False, readonly="1",
            help="Unit of measurement for Weight",),
    }

    _defaults = {
        'weight_uom_id': False
    }


class StockPickingIn(orm.Model):

    _inherit = 'stock.picking.in'

    _columns = {
        'weight_uom_id': fields.many2one(
            'product.uom', 'Unit of Measure', required=False, readonly="1",
            help="Unit of measurement for Weight",),
    }

    _defaults = {
        'weight_uom_id': False
    }


class StockPickingOut(orm.Model):

    _inherit = 'stock.picking.out'

    _columns = {
        'weight_uom_id': fields.many2one(
            'product.uom', 'Unit of Measure', required=False, readonly="1",
            help="Unit of measurement for Weight",),
    }

    _defaults = {
        'weight_uom_id': False
    }


class StockMove(orm.Model):

    _inherit = 'stock.move'

    _columns = {
        'weight_uom_id': fields.many2one(
            'product.uom', 'Unit of Measure', required=False, readonly=True,
            help="Unit of measurement for Weight"),
    }

    _defaults = {
        'weight_uom_id': False
    }
