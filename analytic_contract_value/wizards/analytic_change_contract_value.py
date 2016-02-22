# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _


class AnalyticChangeContractValue(orm.TransientModel):
    _name = "analytic.change.contract.value"
    _description = "Change Contract Value"
    _columns = {
        'new_value': fields.float('New Quantity on Hand',
                                  digits_compute=dp.get_precision('Account'),
                                  required=True)
    }

    def change_contract_value(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        rec_id = context and context.get('active_id', False)
        assert rec_id, _('Active ID is not set in Context')
        analytic_obj = self.pool['account.analytic.account']
        data = self.browse(cr, uid, ids[0], context=context)

        analytic_obj.write(cr, uid, [rec_id], {'contract_value': data[
            'new_value']})
        return {}
