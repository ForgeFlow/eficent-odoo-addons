# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm


class StockPicking(orm.Model):
    
    _inherit = 'stock.picking'

    _columns = {
        'analytic_resource_plan_line_id': fields.many2one(
            'analytic.resource.plan.line', "Resource Plan Line", readonly=True),
    }
