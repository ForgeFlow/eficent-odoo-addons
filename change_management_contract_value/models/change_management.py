# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, orm
from openerp.tools.translate import _


class ChangeManagementChange(orm.Model):
    _inherit = 'change.management.change'

    _columns = {
        'change_value': fields.float('Value',
                                     readonly=True,
                                     help="Value of the Change",
                                     states={'draft': [('readonly', False)]})
    }

    def set_state_accepted(self, cr, uid, ids, *args):
        res = super(ChangeManagementChange, self).set_state_accepted(
            cr, uid, ids)
        analytic_obj = self.pool['account.analytic.account']
        for change in self.browse(cr, uid, ids, context=None):
            if not change.change_project_id:
                raise orm.except_orm(_("Error!"),
                                     _("A Change Management Project must be "
                                       "provided."))
            analytic_obj.write(
                cr, uid, [change.change_project_id.analytic_account_id.id],
                {'contract_value': change.change_value}, context=None)
        return res
