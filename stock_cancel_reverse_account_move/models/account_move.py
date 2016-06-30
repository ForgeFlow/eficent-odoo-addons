# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, osv, orm


class AccountMove(orm.Model):
    _inherit = 'account.move'

    def create_reversal_move(self, cr, uid, move_id, reversal_date,
                             context=None):
        reversal_period_id = self.pool['account.period'].find(
            cr, uid, reversal_date, context=context)[0]
        move_obj = self.pool['account.move']
        move_line_obj = self.pool['account.move.line']
        move = self.browse(cr, uid, move_id, context=context)
        reversal_move_id = move_obj.copy(cr, uid, move_id,
                                         default={'date': reversal_date,
                                                  'period_id':
                                                      reversal_period_id},
                                         context=context)
        move_obj.write(cr, uid, [reversal_move_id], {'ref': move.ref},
                       context=context)
        reversal_move = self.browse(cr, uid, reversal_move_id, context=context)
        for reversal_move_line in reversal_move.line_id:
            move_line_obj.write(
                cr,
                uid,
                [reversal_move_line.id],
                {'debit': reversal_move_line.credit,
                 'credit': reversal_move_line.debit,
                 'amount_currency': reversal_move_line.amount_currency * -1},
                context=context)
        return reversal_move_id
