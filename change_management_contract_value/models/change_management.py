# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, orm
from openerp.tools.translate import _
import time


class ChangeManagementChange(orm.Model):
    _inherit = 'change.management.change'

    _columns = {
        'change_value': fields.float('Value',
                                     readonly=True,
                                     help="Value of the Change",
                                     states={'draft': [('readonly', False)]}),
        'analytic_line_plan_ids': fields.one2many(
            'account.analytic.line.plan',
            'change_id',
            'Revenue planning lines',
            readonly=True,
        ),
        'change_template_id': fields.many2one(
            'change.management.template',
            'Change Template',
            readonly=True,
            states={
                'draft': [('readonly', False)]
            }),
    }

    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'analytic_line_plan_ids': []
        })
        return super(ChangeManagementChange, self).copy(cr, uid, id, default,
                                                        context=context)

    def _prepare_revenue_analytic_line_plan_ids(
            self, cr, uid, change, context=None):
        plan_version_obj = self.pool.get('account.analytic.plan.version')
        res = {}
        res['value'] = {}
        account_id = change.project_id.analytic_account_id
        if not change.change_template_id:
            raise orm.except_orm(_('Sorry'),
                                 _('Change template not found'))
        product_id = change.change_template_id.revenue_product_id
        journal_id = \
            product_id.revenue_analytic_plan_journal_id \
            and product_id.revenue_analytic_plan_journal_id.id \
            or False
        if not journal_id:
            raise orm.except_orm(_('Sorry'),
                                 _('No revenue plan journal for the product'))
        version_id = change.change_template_id.version_id.id or False

        general_account_id = product_id.product_tmpl_id.\
            property_account_income.id
        if not general_account_id:
            general_account_id = product_id.categ_id.\
                property_account_income_categ.id
        if not general_account_id:
            raise orm.except_orm(_('Sorry'),
                                 _('There is no expense account defined '
                                   'for this product: "%s" (id:%d)')
                                 % (product_id.name,
                                    product_id.id,))
        default_plan_ids = plan_version_obj.search(
            cr, uid, [('default_plan', '=', True)],  context=context)
        if default_plan_ids:
            default_plan = plan_version_obj.browse(cr, uid,
                                                   default_plan_ids[0],
                                                   context=context)
        else:
            default_plan = False

        if account_id.active_analytic_planning_version != default_plan:
            raise orm.except_orm(_('Sorry'),
                                 _('The active planning version of the '
                                   'analytic account must be %s. '
                                   '')
                                 % (default_plan.name,))

        return {
            'account_id': account_id.id,
            'name': product_id.name,
            'change_id': change.id,
            'ref': change.name,
            'date': time.strftime('%Y-%m-%d'),
            'product_id': product_id.id,
            'product_uom_id': product_id.uom_id.id,
            'unit_amount': 1,
            'amount': change.change_value,
            'general_account_id': general_account_id,
            'journal_id': journal_id,
            'version_id': version_id,
            'currency_id': account_id.company_id.currency_id.id,
            'amount_currency': change.change_value,
        }

    def create_revenue_plan_lines(
            self, cr, uid, change, context=None):
        res = []
        line_plan_obj = self.pool.get('account.analytic.line.plan')
        line_vals = self._prepare_revenue_analytic_line_plan_ids(
            cr, uid, change, context=context)
        line_id = line_plan_obj.create(cr, uid, line_vals, context=context)
        res.append(line_id)
        return res

    def set_state_accepted(self, cr, uid, ids, *args):
        res = super(ChangeManagementChange, self).set_state_accepted(
            cr, uid, ids, *args)
        self._delete_analytic_lines(cr, uid, ids)
        for change in self.browse(cr, uid, ids):
            line_ids = []
            if not change.change_project_id:
                raise orm.except_orm(_('Sorry'),
                                     _('Change project not provided'))
            line_ids.extend(self.create_revenue_plan_lines(
                cr, uid, change))
        return res

    def _delete_analytic_lines(self, cr, uid, ids, context=None):
        line_plan_obj = self.pool.get('account.analytic.line.plan')
        for change in self.browse(cr, uid, ids, context=context):
            analytic_line_plan_ids = []
            for line in change.analytic_line_plan_ids:
                analytic_line_plan_ids.append(line.id)
            line_plan_obj.unlink(
                cr, uid, analytic_line_plan_ids, context=context)
        return True

    def set_state_draft(self, cr, uid, ids, *args):
        res = super(ChangeManagementChange, self).set_state_draft(
            cr, uid, ids, *args)
        self._delete_analytic_lines(cr, uid, ids)
        return res

    def set_state_rejected(self, cr, uid, ids, *args):
        res = super(ChangeManagementChange, self).set_state_rejected(
            cr, uid, ids, *args)
        self._delete_analytic_lines(cr, uid, ids)
        return res
