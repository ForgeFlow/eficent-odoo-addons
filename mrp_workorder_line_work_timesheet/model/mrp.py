# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time
import datetime

from openerp.osv import fields, orm
from openerp import pooler
from openerp import tools
from openerp.tools.translate import _


class mrp_production_workcenter_line_work(orm.Model):
    _inherit = "mrp.production.workcenter.line.work"
    
    def get_user_related_details(self, cr, uid, user_id):
        res = {}
        emp_obj = self.pool.get('hr.employee')
        emp_id = emp_obj.search(cr, uid, [('user_id', '=', user_id)])
        if not emp_id:
            user_name = self.pool.get('res.users').read(
                cr, uid, [user_id], ['name'])[0]['name']
            raise orm.except_orm(_('Bad Configuration!'), 
                                 _('Please define employee for user "%s". '
                                   'You must create one.')% (user_name,))
        emp = emp_obj.browse(cr, uid, emp_id[0])
        if not emp.product_id:
            raise orm.except_orm(_('Bad Configuration!'),
                                 _('Please define product and product '
                                   'category property account on the '
                                   'related employee.'
                                   '\nFill in the HR Settings tab of the '
                                   'employee form.'))
        if not emp.journal_id:
            raise orm.except_orm(_('Bad Configuration!'),
                                 _('Please define journal on the related '
                                   'employee.'
                                   '\nFill in the timesheet tab of the '
                                   'employee form.'))
        acc_id = emp.product_id.property_account_expense.id
        if not acc_id:
            acc_id = emp.product_id.categ_id.property_account_expense_categ.id
            if not acc_id:
                raise orm.except_orm(_('Bad Configuration!'),
                                     _('Please define product and product '
                                       'category property account on the '
                                       'related employee.'
                                       '\nFill in the timesheet tab of the '
                                       'employee form.'))

        res['product_id'] = emp.product_id.id
        res['journal_id'] = emp.journal_id.id
        res['general_account_id'] = acc_id
        res['product_uom_id'] = emp.product_id.uom_id.id
        return res

    def _create_analytic_entries(self, cr, uid, vals, context):
        """Create the hr analytic timesheet from worcenter actual work"""
        timesheet_obj = self.pool['hr.analytic.timesheet']
        sheet_obj = self.pool['hr_timesheet_sheet.sheet']
        workorder_line_obj = self.pool['mrp.production.workcenter.line']

        vals_line = {}
        timeline_id = False
        acc_id = False

        workorder_line = workorder_line_obj.browse(
            cr, uid, vals['workcenter_line_id'], context=context)
        result = self.get_user_related_details(cr, uid,
                                               vals.get('user_id', uid))
        vals_line['name'] = '%s: %s' % (tools.ustr(workorder_line.name),
                                        tools.ustr(vals['name'] or '/'))
        vals_line['user_id'] = vals['user_id']
        vals_line['product_id'] = result['product_id']
        if vals.get('date'):
            timestamp = datetime.datetime.strptime(
                vals['date'], tools.DEFAULT_SERVER_DATETIME_FORMAT)
            ts = fields.datetime.context_timestamp(cr, uid,
                                                   timestamp, context)
            vals_line['date'] = ts.strftime(tools.DEFAULT_SERVER_DATE_FORMAT)

        # Calculate quantity based on employee's product's uom
        vals_line['unit_amount'] = vals['hours']

        default_uom = self.pool['res.users'].browse(
            cr, uid, uid, context=context).company_id.project_time_mode_id.id
        if result['product_uom_id'] != default_uom:
            vals_line['unit_amount'] = self.pool['product.uom']._compute_qty(
                cr, uid, default_uom, vals['hours'], result['product_uom_id'])
        acc_id = workorder_line.production_id.analytic_account_id.id or False
        if acc_id:
            vals_line['account_id'] = acc_id
            res = timesheet_obj.on_change_account_id(cr, uid, False, acc_id)
            if res.get('value'):
                vals_line.update(res['value'])
            vals_line['general_account_id'] = result['general_account_id']
            vals_line['journal_id'] = result['journal_id']
            vals_line['amount'] = 0.0
            vals_line['product_uom_id'] = result['product_uom_id']
            amount = vals_line['unit_amount']
            prod_id = vals_line['product_id']
            unit = False

            sheet_ids = sheet_obj.search(cr, uid,
                [('date_to', '>=', vals_line['date']),
                 ('date_from', '<=', vals_line['date']),
                 ('employee_id.user_id', '=', vals_line['user_id'])],
                context=context)
            if sheet_ids:
                vals_line['sheet_id'] = sheet_ids[0]
            else:
                raise orm.except_orm(_('Error!'),
                                     _('Employees must have an active '
                                       'Timesheets for the date entered.'
                                       ))
            timeline_id = timesheet_obj.create(cr, uid, vals=vals_line,
                                               context=context)

            # Compute based on pricetype
            amount_unit = timesheet_obj.on_change_unit_amount(
                cr, uid, timeline_id, prod_id, amount, False, unit,
                vals_line['journal_id'], context=context)
            if amount_unit and 'amount' in amount_unit.get('value', {}):
                updv = {'amount': amount_unit['value']['amount']}
                timesheet_obj.write(cr, uid, [timeline_id], updv,
                                    context=context)

        return timeline_id

    def create(self, cr, uid, vals, *args, **kwargs):
        context = kwargs.get('context', {})
        if not context.get('no_analytic_entry', False):
            vals['hr_analytic_timesheet_id'] = \
                self._create_analytic_entries(cr, uid, vals, context=context)
        return super(mrp_production_workcenter_line_work, self).create(
            cr, uid, vals, *args, **kwargs)

    def write(self, cr, uid, ids, vals, context=None):
        """
        When work gets updated, handle its hr analytic timesheet.
        """
        if context is None:
            context = {}
        timesheet_obj = self.pool.get('hr.analytic.timesheet')
        uom_obj = self.pool.get('product.uom')
        result = {}

        if isinstance(ids, (long, int)):
            ids = [ids]

        for line_work in self.browse(cr, uid, ids, context=context):
            line_id = line_work.hr_analytic_timesheet_id
            if not line_id:
                # if a record is deleted from timesheet,
                # the line_id will become
                # null because of the foreign key on-delete=set null
                continue

            vals_line = {}
            if 'name' in vals:
                vals_line['name'] = \
                    '%s: %s' % (
                        tools.ustr(line_work.workcenter_line_id.name),
                        tools.ustr(vals['name'] or '/')
                    )
            if 'user_id' in vals:
                vals_line['user_id'] = vals['user_id']
            if 'date' in vals:
                vals_line['date'] = vals['date'][:10]
            if 'hours' in vals:
                vals_line['unit_amount'] = vals['hours']
                prod_id = vals_line.get(
                    'product_id', line_id.product_id.id)  # False may be set

                # Put user related details in analytic timesheet values
                details = self.get_user_related_details(
                    cr, uid, vals.get('user_id', line_work.user_id.id))
                for field in ('product_id', 'general_account_id',
                              'journal_id', 'product_uom_id'):
                    if details.get(field, False):
                        vals_line[field] = details[field]

                # Check if user's default UOM differs from product's UOM
                user_default_uom_id = self.pool.get('res.users').browse(
                    cr, uid, uid).company_id.project_time_mode_id.id
                if details.get('product_uom_id', False) \
                        and details['product_uom_id'] != user_default_uom_id:
                    vals_line['unit_amount'] = uom_obj._compute_qty(
                        cr, uid, user_default_uom_id, vals['hours'],
                        details['product_uom_id'])

                # Compute based on pricetype
                amount_unit = timesheet_obj.on_change_unit_amount(
                    cr, uid, line_id.id, prod_id=prod_id, company_id=False,
                    unit_amount=vals_line['unit_amount'], unit=False,
                    journal_id=vals_line['journal_id'], context=context)

                if amount_unit and 'amount' in amount_unit.get('value',{}):
                    vals_line['amount'] = amount_unit['value']['amount']

            if vals_line:
                self.pool.get('hr.analytic.timesheet').write(cr, uid, [line_id.id], vals_line, context=context)

        return super(mrp_production_workcenter_line_work, self).write(
            cr, uid, ids, vals, context)

    def unlink(self, cr, uid, ids, *args, **kwargs):
        hat_obj = self.pool.get('hr.analytic.timesheet')
        hat_ids = []
        for workcenter_line_work in self.browse(cr, uid, ids):
            if workcenter_line_work.hr_analytic_timesheet_id:
                hat_ids.append(
                    workcenter_line_work.hr_analytic_timesheet_id.id)
        # Delete entry from timesheet too while deleting entry
        # to worcenter line.
        if hat_ids:
            hat_obj.unlink(cr, uid, hat_ids, *args, **kwargs)
        return super(mrp_production_workcenter_line_work, self).unlink(
            cr, uid, ids, *args, **kwargs)

    _columns = {
        'hr_analytic_timesheet_id': fields.many2one('hr.analytic.timesheet',
                                                    'Related Timeline Id',
                                                    ondelete='set null'),
    }