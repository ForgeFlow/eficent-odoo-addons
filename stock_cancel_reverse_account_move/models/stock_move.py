# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, osv, orm


class StockMove(orm.Model):
    _inherit = 'stock.move'

    def write(self, cr, uid, ids, vals, context=None):
        if 'state' in vals:
            am_obj = self.pool['account.move']
            aml_obj = self.pool['account.move.line']

            for sm in self.browse(cr, uid, ids, context=context):
                if sm.state == 'done' and vals['state'] != 'done':
                    aml_ids = aml_obj.search(cr, uid, [('sm_id', '=', sm.id)],
                                             limit=1, context=context)
                    am_id = False
                    for aml in aml_obj.browse(cr, uid, aml_ids,
                                              context=context):
                        am_id = aml.move_id.id
                    if am_id:
                        move_date = fields.date.context_today(self, cr, uid,
                                                              context=context)
                        am_obj.create_reversal_move(
                            cr, uid, am_id, move_date, context=context)

        return super(StockMove, self).write(cr, uid, ids, vals,
                                            context=context)
