# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError

_REQUEST_STATE = [
    ('none', 'No Request'),
    ('draft', 'Draft'),
    ('to_approve', 'To be approved'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected')
]


class AnalyticResourcePlanLine(models.Model):

    _inherit = 'analytic.resource.plan.line'

    @api.multi
    @api.depends('purchase_request_lines')
    def _requested_qty(self):
        for line in self:
            requested_qty = 0.0
            for purchase_line in line.purchase_request_lines:
                if purchase_line.request_id.state != 'rejected':
                    requested_qty += purchase_line.product_qty
            line.requested_qty = requested_qty
        return True

    @api.multi
    @api.depends('purchase_request_lines.request_id.state')
    def _get_request_state(self):
        for line in self:
            line.request_state = 'none'
            if line.purchase_request_lines:
                if any([pr_line.request_id.state == 'approved' for pr_line in
                        line.purchase_request_lines]):
                    line.request_state = 'approved'
                elif all([pr_line.request_id.state == 'rejected' for pr_line in
                          line.purchase_request_lines]):
                    line.request_state = 'rejected'
                elif all([pr_line.request_id.state in ('to_approve', 'cancel')
                          for pr_line in line.purchase_request_lines]):
                    line.request_state = 'to_approve'
                elif any([pr_line.request_id.state == 'approved' for pr_line in
                          line.purchase_request_lines]):
                    line.request_state = 'approved'
                elif all([pr_line.request_id.state in ('draft', 'cancel')
                          for pr_line in line.purchase_request_lines]):
                    line.request_state = 'draft'
        return True

    requested_qty = fields.Float(
        compute=_requested_qty,
        string='Requested quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        readonly=True)

    request_state = fields.Selection(
        compute=_get_request_state, string='Request status',
        selection=_REQUEST_STATE,
        store=True,
        default='none')
    purchase_request_lines = fields.Many2many(
        'purchase.request.line',
        'purchase_request_line_analytic_resource_plan_line_line_rel',
        'analytic_resource_plan_line_id',
        'purchase_request_line_id',
        string='Purchase Request Lines',
        copy=False,
        readonly=True)
    label = fields.Char('Label to PR',
                        readonly=True, states={'draft': [('readonly', False)]})

    @api.multi
    def unlink(self):
        for line in self:
            if line.purchase_request_lines.filtered(
                    lambda l: l.request_state not in('rejected')):
                raise ValidationError(
                    _('You cannot delete plan lines that refers to '
                      'not rejected Purchase request lines'))
        return super(AnalyticResourcePlanLine, self).unlink()

    @api.multi
    def action_button_draft(self):
        res = super(AnalyticResourcePlanLine, self).action_button_draft()
        for line in self:
            for request_line in line.purchase_request_lines:
                request_line.request_id.button_rejected()
        return res

    @api.multi
    def action_button_confirm(self):
        res = super(AnalyticResourcePlanLine, self).action_button_confirm()
        self._make_purchase_request()
        return res

    @api.model
    def _prepare_purchase_request(self, company_id, picking_type_id=None,
                                  line=None):
        data = {
            'company_id': company_id,
            'origin': self.label or line.account_id.name if line else self.name,
            'description': self.product_id.description,
            'picking_type_id': picking_type_id,
        }
        return data

    def _prepare_purchase_request_line(self, pr_id, line):
        return {
            'request_id': pr_id.id,
            'name': self.product_id.name,
            'product_qty': line.unit_amount,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom_id.id,
            'date_required': self.date or False,
            'analytic_account_id': self.account_id.id,
            'analytic_resource_plan_lines': [(4, self.id)]
        }

    @api.multi
    def _make_purchase_request(self):
        request_obj = self.env['purchase.request']
        request_line_obj = self.env['purchase.request.line']
        company_id = False
        warehouse_id = False
        children = self._get_child_resource_plan_lines()
        for line in self.browse(children):
            if line.child_ids:
                continue
            line_company_id = line.account_id.company_id.id or False
            if company_id is not False \
                    and line_company_id != company_id:
                raise ValidationError(
                    _('You have to select lines '
                      'from the same company.'))
            else:
                company_id = line_company_id
            line_warehouse_id = \
                line.account_id.picking_type_id.warehouse_id or False
            if warehouse_id is not False \
                    and line_warehouse_id != warehouse_id:
                raise ValidationError(
                    _('You have to select lines '
                      'from the same warehouse.'))
            else:
                warehouse_id = line_warehouse_id
            picking_type_id = line.account_id.picking_type_id
            if not picking_type_id:
                raise ValidationError(
                    _("No picking type defined for the analytic account"))
            request_data = line._prepare_purchase_request(
                company_id, picking_type_id.id, line)
            request_id = request_obj.create(request_data)
            request_line_data = line._prepare_purchase_request_line(
                request_id, line)
            request_line_id = request_line_obj.create(
                request_line_data)
            line.purchase_request_lines = [(4, request_line_id.id)]
        return True
