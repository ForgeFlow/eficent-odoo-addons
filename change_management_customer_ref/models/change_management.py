# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, orm


class ChangeManagementChange(orm.Model):
    _inherit = 'change.management.change'

    def _get_change_orders_project(self, cr, uid, ids, context=None):
        result = set()
        project_obj = self.pool['project.project']
        for order in project_obj.browse(cr, uid, ids, context=context):
            for change in order.change_ids:
                result.add(change.id)
        return list(result)

    _columns = {

        'customer_id':  fields.related('project_id', 'partner_id',
                                       type='many2one', relation='res.partner',
                                       string='Customer',
                                       readonly=True,
                                       store={
                                           'project.project': (
                                               _get_change_orders_project,
                                               ['partner_id'], 20)}),

        'customer_ref': fields.char('Customer ref.',
                                    help="Reference of the Change as "
                                         "indicated by the Customer",
                                    readonly=True,
                                    states={'draft': [('readonly', False)]})
    }
