# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError
from datetime import datetime


class AnalyticResourcePlanLineStockPickingOut(models.TransientModel):
    _name = "analytic.resource.plan.line.stock.picking.out"
    _description = "Resource plan make delivery order"

    def _default_date(self):
        return datetime.now()

    date = fields.Datetime(
        'Picking date', help="Picking date", required=True,
        default=_default_date)
    date_expected = fields.Datetime(
        'Scheduled Date', required=True,
        help="Scheduled date for the processing of the move.")
    item_ids = fields.One2many(
        'analytic.resource.plan.line.stock.picking.out.item',
        'picking_out_wiz_id', 'Items')
    move_type = fields.Selection([
        ('direct', 'Partial'), ('one', 'All at once')], 'Delivery Type',
        default='direct', required=True,
        help="It specifies goods to be deliver partially or all at once")

    def _prepare_item(self, line):
        return {
            'product_id': line.product_id.id,
            'product_qty': line.unit_amount,
            'product_uom_id': line.product_uom_id.id,
            'line_id': line.id,
        }

    @api.model
    def default_get(self, fields):
        res = super(
            AnalyticResourcePlanLineStockPickingOut, self).default_get(fields)
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

    def _prepare_order_move(self, item, picking_id, date, date_expected):
        line = item.line_id
        location_id = line.account_id.location_id.id
        partner_id = line.account_id.dest_address_id.id
        product_uom_id = line.product_uom_id.id
        wh = line.account_id.location_id.get_warehouse()

        return {
            'name': line.name,
            'picking_id': picking_id.id,
            'product_id': line.product_id.id,
            'date': date,
            'date_expected': date_expected,
            'product_uom': product_uom_id,
            'product_uom_qty': line.unit_amount,
            'product_uos': product_uom_id,
            'partner_id': partner_id,
            'location_id': location_id,
            'location_dest_id': wh.wh_output_stock_loc_id.id,
            'analytic_account_id': line.account_id.id,
            'tracking_id': False,
            'state': 'draft',
            'company_id': line.account_id.company_id.id,
            'price_unit': 0.0
        }

    def _prepare_order_picking(self, line, date, move_type):
        pick_name = self.env['ir.sequence'].next_by_code('stock.picking.out')
        type_obj = self.env['stock.picking.type']
        company_id = self.env.context.get('company_id') or self.env.user.company_id.id
        types = type_obj.search([('code', '=', 'incoming'), ('warehouse_id.company_id', '=', company_id),
                                 ('name', '=', 'Receptions'),
                                 ('warehouse_id.operating_unit_id', '=', self.env.user.default_operating_unit_id.id)])
        picking_type = types[:1]
        location = line.account_id.location_id

        wh = line.account_id.location_id.get_warehouse()
        return {
            'name': pick_name,
            'origin': line.account_id.name,
            'date': date,
            'type': 'out',
            'state': 'draft',
            'move_type': move_type,
            'location_id': location.id,
            'operating_unit_id': location.operating_unit_id.id,
            'location_dest_id': wh.wh_output_stock_loc_id.id,
            'picking_type_id': picking_type.id,
            'partner_id': line.account_id.dest_address_id and
            line.account_id.dest_address_id.id or False,
            'invoice_state': 'none',
            'company_id': line.account_id.company_id.id,
        }

    @api.multi
    def make_stock_picking_out(self):
        res = []
        make_picking = self
        picking_obj = self.env['stock.picking']
        move_obj = self.env['stock.move']
        company_id = False
        dest_address_id = False
        picking_id = False

        for item in make_picking.item_ids:
            line = item.line_id
            line_dest_address_id = line.account_id.dest_address_id \
                and line.account_id.dest_address_id.id or False
            if not line_dest_address_id:
                raise ValidationError(
                    _('You have to select lines '
                      'with a delivery address defined in the '
                      'Project / Analytic Account.'))

            if dest_address_id is not False \
                    and line_dest_address_id != dest_address_id:
                raise ValidationError(
                    _('You have to select lines '
                      'with the same delivery address.'))
            else:
                dest_address_id = line_dest_address_id

            project = self.env['project.project'].search(
                [('analytic_account_id', '=', line.account_id.id)], limit=1)
            if make_picking.date_expected < project.date_start:
                raise ValidationError(
                    _('The expected date must be after the '
                      'Project start date.'))
            if line.state != 'confirm':
                raise ValidationError(
                    _('All resource plan lines must be  '
                      'confirmed.'))
            if line.product_id \
                    and line.product_id.type not in ('product', 'consu'):
                raise ValidationError(
                    _('You have to select stockable or '
                      'consumable items.'))
            line_company_id = line.account_id.company_id \
                and line.account_id.company_id.id or False
            if company_id is not False \
                    and line_company_id != company_id:
                raise ValidationError(
                    _('You have to select lines '
                      'from the same company.'))
            else:
                company_id = line_company_id

            if picking_id is False:
                picking_id = picking_obj.create(
                    self._prepare_order_picking(
                        line, make_picking.date,
                        make_picking.move_type))
            move_data = self._prepare_order_move(
                item, picking_id, make_picking.date,
                make_picking.date_expected)
            move_obj.create(move_data)
            res.append(picking_id.id)
            picking_id.action_confirm()

        return {
            'domain': "[('id','in', ["+','.join(map(str, res))+"])]",
            'name': _('Delivery Orders'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }


class AnalyticResourcePlanLineStockPickingOutItem(models.TransientModel):
    _name = "analytic.resource.plan.line.stock.picking.out.item"
    _description = "Resource plan make delivery order item"

    picking_out_wiz_id = fields.Many2one(
        'analytic.resource.plan.line.stock.picking.out',
        'Picking Wizard', required=True, ondelete='cascade',
        readonly=True)
    line_id = fields.Many2one('analytic.resource.plan.line',
                              'Resource Plan Line',
                              required=True,
                              readonly=True)
    product_qty = fields.Float(string='Quantity to deliver',
                               digits=dp.get_precision('Product UoS'))
    product_uom_id = fields.Many2one(related='line_id.product_uom_id')
