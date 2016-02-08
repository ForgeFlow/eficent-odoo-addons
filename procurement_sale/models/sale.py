# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm, fields


class SaleOrder(orm.Model):
    _inherit = "sale.order"

    def _prepare_order_line_procurement(self, cr, uid, order, line, move_id,
                                        date_planned, context=None):
        res = super(
            SaleOrder, self)._prepare_order_line_procurement(
                cr, uid, order, line,
                move_id, date_planned,
                context)
        res['sale_order_line_id'] = line.id
        return res
