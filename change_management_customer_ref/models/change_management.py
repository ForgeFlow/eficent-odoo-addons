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

    def _get_project_customer(self, cr, uid, ids, field_name, arg,
                              context=None):
        result = {}
        for change in self.browse(cr, uid, ids, context=context):
            result[change.id] = change.project_id.partner_id.id
        return result

    def _search_by_project_customer(self, cr, uid, obj, name, args, context):
        change_ids = {}
        for cond in args:
            partner_id = cond[2]
            project_ids = self.pool['project.project'].search(
                cr, uid, [('partner_id', '=', partner_id)])
            change_ids = self.pool['change.management.change'].search(
                cr, uid, [('project_id', 'in', project_ids)])
        if change_ids:
            return [('id', 'in', tuple(change_ids))]
        else:
            return False

    _columns = {

        'customer_id':  fields.function(
            _get_project_customer, method=True, type='many2one',
            relation='res.partner', string='Customer', readonly=True,
            store=False, fnct_search=_search_by_project_customer),

        'customer_ref': fields.char('Customer ref.',
                                    help="Reference of the Change as "
                                         "indicated by the Customer",
                                    readonly=True,
                                    states={'draft': [('readonly', False)]})
    }
