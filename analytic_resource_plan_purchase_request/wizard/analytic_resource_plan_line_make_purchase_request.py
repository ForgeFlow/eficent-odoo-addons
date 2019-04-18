# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.
from odoo import _, api, fields, models
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError


class AnalyticResourcePlanLineMakePurchaseRequest(models.TransientModel):
    _name = "analytic.resource.plan.line.make.purchase.request"
    _description = "Resource plan make purchase request"

    origin = fields.Char('Origin', size=32, required=True)
    description = fields.Text('Description')
    item_ids = fields.One2many(
        'analytic.resource.plan.line.make.purchase.request.item',
        'wiz_id', 'Items')

    @api.model
    def _prepare_item(self, line):
        return {
            'account_id': line.account_id.id,
            'product_id': line.product_id.id,
            'product_qty': line.unit_amount,
            'product_uom_id': line.product_uom_id.id,
            'line_id': line.id,
        }

    @api.model
    def default_get(self, fields):
        res = super(AnalyticResourcePlanLineMakePurchaseRequest,
                    self).default_get(fields)
        res_plan_obj = self.env['analytic.resource.plan.line']
        resource_plan_line_ids = self.env.context.get('active_ids', [])
        active_model = self.env.context.get('active_model')

        if not resource_plan_line_ids:
            return res
        assert active_model == 'analytic.resource.plan.line', \
            'Bad context propagation'

        items = []
        for line in res_plan_obj.browse(resource_plan_line_ids):
            items.append([0, 0, self._prepare_item(line)])
        res['item_ids'] = items
        return res

    @api.model
    def _prepare_purchase_request(self, make_purchase_request,
                                  company_id):
        data = {
            'company_id': company_id,
            'origin': make_purchase_request.origin,
            'description': make_purchase_request.description,
            }
        return data

    @api.model
    def _prepare_purchase_request_line(self, pr_id, item):
        return {
            'request_id': pr_id,
            'name': item.product_id.name,
            'product_qty': item.product_qty,
            'product_id': item.product_id.id,
            'product_uom_id': item.product_uom_id.id,
            'date_required': item.line_id.date or False,
            'analytic_account_id': item.line_id.account_id.id,
            'analytic_resource_plan_lines': [(4, item.line_id.id)]
        }

    @api.multi
    def make_purchase_request(self):
        res = []
        make_purchase_request = self
        line_plan_obj = self.env['analytic.resource.plan.line']
        request_obj = self.env['purchase.request']
        request_line_obj = self.env['purchase.request.line']
        company_id = False
        request = False
        for item in make_purchase_request.item_ids:
            line = item.line_id
            if item.product_qty < 0.0:
                raise ValidationError(
                    _('Enter a positive quantity.'))

            line_company_id = line.account_id.company_id \
                and line.account_id.company_id.id or False
            if company_id is not False \
                    and line_company_id != company_id:
                raise ValidationError(
                    _('You have to select lines '
                      'from the same company.'))
            else:
                company_id = line_company_id

            if not len(line.account_id.location_id):
                raise ValidationError(
                    _('The analytic account has no location assigned'))
            picking_type_id = line.account_id.picking_type_id
            if not len(picking_type_id):
                raise ValidationError(
                    _("No picking type defined for the analytic account"))
            if request is False:
                request_data = self._prepare_purchase_request(
                    make_purchase_request, company_id)
                request = request_obj.create(request_data)
            request_line_data = self._prepare_purchase_request_line(
                request.id, item)
            request_line = request_line_obj.create(request_line_data)
            values = {
                'purchase_request_lines': [(4, request_line.id)],
                'state': 'confirm'
            }
            line.write(values)
            project_manager_id = line.account_id.user_id and \
                line.account_id.user_id.partner_id.id or False
            res.append(request_line.id)

        return {
            'domain': "[('id','in', [" + ','.join(map(str, res)) + "])]",
            'name': _('Purchase Request Lines'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.request.line',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }


class AnalyticResourcePlanLineMakePurchaseRequestItem(models.TransientModel):
    _name = "analytic.resource.plan.line.make.purchase.request.item"
    _description = "Resource plan make purchase request item"

    wiz_id = fields.Many2one(
            'analytic.resource.plan.line.make.purchase.request',
            'Wizard', required=True, ondelete='cascade',
            readonly=True)
    line_id = fields.Many2one('analytic.resource.plan.line',
                              'Resource Plan Line',
                               required=True,
                               readonly=True)
    account_id = fields.Many2one('account.analytic.account',
                                 related='line_id.account_id',
                                 string='Analytic Account',
                                 readonly=True)
    product_id = fields.Many2one('product.product',
                                 related='line_id.product_id',
                                 string='Product',
                                 readonly=True)
    product_qty = fields.Float(string='Quantity to request',
                               digits=dp.get_precision('Product UoS'))
    product_uom_id = fields.Many2one('product.uom',
                                     related='line_id.product_uom_id',
                                     string='UoM',
                                     readonly=True)
