# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp


class AnalyticResourcePlanLineConsume(models.TransientModel):
    _name = "analytic.resource.plan.line.consume"
    _description = "Consume from Resource Plan Lines"

    item_ids = fields.One2many(
        'analytic.resource.plan.line.consume.item',
        'wiz_id',
        'Items'
    )

    def _prepare_item(self, line):
        return {
            'product_qty': line.unit_amount,
            'product_uom_id': line.product_uom_id.id,
            'line_id': line.id,
        }

    @api.model
    def default_get(self, fields):
        res = super(AnalyticResourcePlanLineConsume, self).default_get(fields)
        res_plan_obj = self.env['analytic.resource.plan.line']
        resource_plan_line_ids = self._context.get('active_ids', [])
        active_model = self._context.get('active_model')

        if not resource_plan_line_ids:
            return res
        assert active_model == 'analytic.resource.plan.line', \
            'Bad context propagation'

        items = []
        for line in res_plan_obj.browse(resource_plan_line_ids):
            items.append((0, 0, self._prepare_item(line)))
        res.update({'item_ids': items})
        return res

    def do_consume(self):
        res = []
        res_plan_obj = self.env['analytic.resource.plan.line']
        for item in self.item_ids:
            if item.product_qty > item.line_id.qty_available:
                raise UserError(
            ("Cannot consume material for product '%s'. Not enough stock" % (
                item.line_id.product_id.name)))
            move_id = res_plan_obj.create_consume_move(item.line_id.id,
                                                       item.product_qty)
            res.append(move_id.id)
        return {
            'domain': "[('id','in', ["+','.join(map(str, res))+"])]",
            'name': _('Stock Moves'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.move',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }


class AnalyticResourcePlanLineConsumeItem(models.TransientModel):
    _name = "analytic.resource.plan.line.consume.item"
    _description = "Resource plan consume item"

    wiz_id = fields.Many2one(
        'analytic.resource.plan.line.consume',
        'Wizard',
        required=True,
        ondelete='cascade',
        readonly=True
    )
    line_id = fields.Many2one(
        'analytic.resource.plan.line',
        'Resource Plan Line',
        required=True,
        readonly=True
    )
    product_qty = fields.Float(
        string='Quantity to consume',
        digits=dp.get_precision('Product UoS')
    )
    product_uom_id = fields.Many2one(
        'product.uom',
        related='line_id.product_uom_id',
        string='UoM',
        readonly=True
    )
