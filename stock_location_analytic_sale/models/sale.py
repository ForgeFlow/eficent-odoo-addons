# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm


class SaleOrder(orm.Model):
    _inherit = "sale.order"

    def _get_default_location(self, cr, uid, id, context=None):
        if context is None:
            context = {}
        res = False
        project = self.browse(cr, uid, id, context)
        if project:
            location_id = self.pool.get('stock.location').search(
                cr, uid, [('analytic_account_id', '=', project.id)])
            if location_id:
                res['location_id'] = location_id[0]
        return res

    def _check_location(self, cr, uid, ids, context=None):
        for sale in self.browse(cr, uid, ids):
            if sale.location_id:
                if sale.location_id.analytic_account_id != sale.project_id:
                    return False
        return True

    _columns = {
        'location_id': fields.many2one(
            'stock.location', 'Source Location', select=True,
            domain="[('project_id.location_id','=',True)]")
    }

    _defaults = {
        'location_id': _get_default_location,
    }

    _constraints = [(_check_location, "The location does not have the same"
                                      " project",
                     ['analytic_account_id'])]

    # def _prepare_order_line_move(self, cr, uid, order, line, picking_id,
    #                              date_planned, context=None):
    #     res = super(SaleOrder, self)._prepare_order_line_move(
    #         cr, uid, order, line, picking_id, date_planned, context)
    #     res['analytic_account_id'] = \
    #         line.order_id and line.order_id.project_id \
    #         and line.order_id.project_id.id
    #     if order.project_id:
    #         res['location_id'] = order.location_id.id or \
    #                              order.project_id.location_id.id
    #     return res
