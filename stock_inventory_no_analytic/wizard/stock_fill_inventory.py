# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, osv, orm


class StockFillInventory(orm.TransientModel):
    _inherit = "stock.fill.inventory"

    _columns = {
        'no_analytic': fields.boolean('Only stock not linked to an Analytic '
                                      'Account',
                                      required=False)
    }

    _defaults = {
        'no_analytic': False,
    }

    def _get_search_criteria(self, cr, uid, ids, location, context):
        for fill_inventory in self.browse(cr, uid, ids, context=context):
            search_criteria = ['|', ('location_dest_id', '=', location),
                               ('location_id', '=', location),
                               ('state', '=', 'done')]
            if fill_inventory.no_analytic:
                search_criteria.extend(
                    [('analytic_account_id', '=', False)])
            else:
                if fill_inventory.analytic_account_id:
                    search_criteria = super(StockFillInventory, self).\
                        _get_search_criteria(cr, uid, ids, location, context)
            return search_criteria
