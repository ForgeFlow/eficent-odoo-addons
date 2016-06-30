# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import osv, fields, orm


class StockMove(orm.Model):
    _inherit = 'stock.move'

    _columns = {
        'order_line_sequence': fields.integer(
            string='Order Seq.',
            readonly=True,
            help='Field to show the sequence number of the sales/purchase '
                 'order line.')
    }
