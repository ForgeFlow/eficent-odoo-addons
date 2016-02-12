# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm


class StockWarehouse(orm.Model):

    _inherit = 'stock.warehouse'

    _columns = {

        'wh_analytic_reserve_location_id': fields.many2one(
            'stock.location', 'Stock Analytic Reservation Location',
            help="This is an inventory location that will be used when making "
                 "stock reservations for an analytic account. Should be "
                 "different from the one used to report inventory adjustments."
                 "If you use real-time inventory "
                 "valuation, please make sure that the GL accounts defined "
                 "in this location are the same for Debit and "
                 "Credit, and classified as Balance Sheet accounts.",
            domain=[('usage', '=', 'inventory')]),
    }

    def copy_data(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}
        default['analytic_reserve_location_id'] = False
        res = super(StockWarehouse, self).copy_data(
            cr, uid, id, default, context)
        return res
