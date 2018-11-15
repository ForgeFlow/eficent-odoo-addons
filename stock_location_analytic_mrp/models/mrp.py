# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm


class MrpProduction(orm.Model):
    _inherit = 'mrp.production'

    def _check_mrp_location(self, cr, uid, ids, context=None):
        for mrp in self.browse(cr, uid, ids):
            if mrp.analytic_account_id:
                analytic = mrp.analytic_account_id
                if (mrp.location_src_id.analytic_account_id != analytic or
                        mrp.location_dest_id.analytic_account_id != analytic):
                    return False
        return True

    _constraints = [(_check_mrp_location,
                     "The location does not belong to this project",
                     ['analytic_account_id', 'location_src_id',
                      'location_dest_id'])]
