# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, orm


class AccountAnalyticAccount(orm.Model):
    _inherit = 'account.analytic.account'

    def write(self, cr, uid, ids, values, context=None):
        for project_id in ids:
            project = self.browse(cr, uid, project_id)
            if values.get('stage_id', False):
                stage_obj = self.pool['analytic.account.stage']
                stage = stage_obj.browse(cr, uid, values['stage_id'],
                                         context=context)
                if stage.use_timesheets and project.account_class == \
                        'work_package':
                    values['use_timesheets'] = True
                else:
                    values['use_timesheets'] = False
                values['use_timesheets'] = False
        return super(AccountAnalyticAccount, self).write(cr, uid, ids,
                                                         values,
                                                         context=context)
