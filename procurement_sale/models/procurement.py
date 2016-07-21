# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, orm
from openerp.tools.translate import _


class Procurement(orm.Model):
    _inherit = 'procurement.order'
    _columns = {
        'sale_order_line_id': fields.many2one(
            'sale.order.line', 'Sale Order Line'),
    }
