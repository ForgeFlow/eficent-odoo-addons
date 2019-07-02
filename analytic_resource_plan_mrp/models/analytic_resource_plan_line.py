# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AnalyticResourcePlanLine(models.Model):
    _inherit = 'analytic.resource.plan.line'

    @api.multi
    def _compute_show_button_bom_explode(self):
        for line in self:
            if line.bom_id:
                line.show_button_bom_explode = True
            else:
                line.show_button_bom_explode = False

    @api.multi
    def action_button_confirm(self):
        for line in self:
            if line.bom_id:
                line.bom_explode_to_resource_plan()
        return super(AnalyticResourcePlanLine, self).action_button_confirm()

    bom_id = fields.Many2one(
        'mrp.bom',
        'Bill of Materials',
        readonly=True,
        required=False,
        states={'draft': [('readonly', False)]}
    )
    show_button_bom_explode = fields.Boolean(
        string='show button bom explode',
        compute='_compute_show_button_bom_explode',
    )

    @api.onchange('product_id')
    def on_change_product_id(self):
        super(AnalyticResourcePlanLine, self).on_change_product_id()
        bom_obj = self.env['mrp.bom']
        bom_id = bom_obj._bom_find(product=self.product_id)
        self.bom_id = bom_id

    @api.multi
    def button_bom_explode_to_resource_plan(self):
        res = self.bom_explode_to_resource_plan()
        return {
            'domain': "[('id','in', [" + ','.join(map(str, res)) + "])]",
            'name': _('New Resource Plan Lines'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'analytic.resource.plan.line',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }

    def _prepare_resource_plan_line(self, plan, line, new_qty):
        bom_obj = self.env['mrp.bom']
        bom_id = bom_obj._bom_find(product=line.product_id)
        res = {
            'account_id': plan.account_id.id,
            'name': line.product_id.name,
            'date': plan.date,
            'state': 'draft',
            'product_id': line.product_id.id,
            'product_uom_id': line.product_id.uom_id.id,
            'unit_amount': new_qty * plan.unit_amount,
            'price_unit': line.product_id.standard_price,
            'bom_id': bom_id.id,
            'parent_id': plan.id,
            'resource_type': 'procurement',
        }
        if line.product_id.uom_id.name == 'Hour(s)':
            res.update({'resource_type': 'task'})
        return res

    @api.multi
    def bom_explode_to_resource_plan(self):
        plan_line_obj = self.env['analytic.resource.plan.line']
        res = []
        for plan in self:
                # Search for child resource plan lines.
            plan_line_ids = plan_line_obj.\
                search([('parent_id', '=', plan.id),
                        ('state', '=', 'draft')])
            plan_line_ids.unlink()
            factor = plan.product_uom_id.\
                _compute_quantity(plan.unit_amount,
                                  plan.product_uom_id,
                                  plan.bom_id.product_uom_id)
            bom_res = plan.bom_id.explode(plan.product_id,
                                          factor / plan.bom_id.product_qty,
                                          picking_type=False)
            for component in bom_res[1]:
                line = component[0]
                plan_line_ids = plan_line_obj.\
                    search([('parent_id', '=', plan.id),
                            ('product_id', '=', line.product_id.id),
                            ('state', '!=', 'draft')],)
                total_qty = 0.0
                for plan_line in plan_line_ids:
                    total_qty += plan_line.unit_amount

                if line.product_qty > total_qty:
                    new_qty = line.product_qty - total_qty
                    resource_line_data =\
                        self._prepare_resource_plan_line(plan, line,
                                                         new_qty)
                    plan_id = plan_line_obj.create(resource_line_data)
                    res.append(plan_id.id)
        return res

    def _prepare_consume_move(self, line, product_qty):
        if line.product_id.type not in ('product', 'consu'):
            raise ValidationError(_('''The product must be stockable or
                consumable.'''))
        if product_qty <= 0:
            raise ValidationError(_('''The quantity to consume must be greater
                or equal to 0.'''))

        if line.state != 'confirm':
            raise ValidationError(_('''The resource plan line must be
                confirmed.'''))

        destination_location_id = line.product_id.property_stock_production.id
        if not line.account_id.location_id:
            raise ValidationError(_('''The analytic account must contain a
                default Location.'''))

        source_location_id = line.account_id.location_id.id
        move_data = {
            'name': line.name,
            'date': line.date,
            'product_id': line.product_id.id,
            'product_uom_qty': product_qty,
            'product_uom': line.product_uom_id.id,
            'location_id': source_location_id,
            'location_dest_id': destination_location_id,
            'state': 'assigned',
            'company_id': line.account_id.company_id.id,
            'analytic_account_id': line.account_id.id,
        }
        return move_data

    def _create_stock_move(self, move_data):
        stock_move = self.env['stock.move']
        return stock_move.create(move_data)

    def _complete_stock_move(self, move_id):
        return move_id.action_done()

    def create_consume_move(self, line_id, product_qty):
        line = self.browse(line_id)
        move_data = self._prepare_consume_move(line, product_qty)
        move_id = False
        if move_data:
            move_id = self._create_stock_move(move_data)
            self._complete_stock_move(move_id)
        return move_id

    def _prepare_produce_move(self, line, product_qty):
        if line.product_id.type not in ('product', 'consu'):
            raise ValidationError(_('''The product must be stockable or
                consumable.'''))
        if product_qty <= 0:
            raise ValidationError(_('''The quantity to produce must be greater
                or equal to 0.'''))
        if line.state != 'confirm':
            raise ValidationError(_('''The resource plan line must be
                confirmed.'''))
        source_location_id = line.product_id.property_stock_production.id
        if not line.account_id.location_id:
            raise ValidationError(_('''The analytic account must contain a
                default Location.'''))
        destination_location_id = line.account_id.location_id.id
        move_data = {
            'name': line.name,
            'date': line.date,
            'product_id': line.product_id.id,
            'product_uom_qty': product_qty * line.unit_amount,
            'product_uom': line.product_uom_id.id,
            'location_id': source_location_id,
            'location_dest_id': destination_location_id,
            'state': 'assigned',
            'company_id': line.account_id.company_id.id,
            'analytic_account_id': line.account_id.id,
        }
        return move_data

    def _create_produce_move(self, move_data):
        stock_move = self.env['stock.move']
        return stock_move.create(move_data)

    def create_produce_move(self, line_id, product_qty):
        line = self.browse(line_id)
        move_data = self._prepare_produce_move(line, product_qty)
        move_id = False
        if move_data:
            move_id = self._create_stock_move(move_data)
            self._complete_stock_move(move_id)
        return move_id
