# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import _, api, fields, models
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import UserError
import time


class AnalyticResourcePlanLine(models.Model):

    _inherit = 'analytic.resource.plan.line'

    @api.multi
    def _get_product_available(self, location):

        """ Finds the incoming and outgoing quantity of product on the
        for that analytic account and the location defaulted in the analytic
        account.
        @return: Dictionary of values
        """
        res = {}

        for line in self:
            if line.product_id.type == 'service':
                continue
            c = self.env.context.copy()
            c.update({'states': ('done',), 'what': ('in', 'out'),
                      'location': location})

            stock = self.with_context(c).env['product.product'].\
                _product_available(line.product_id.id)
            res[line.id] = stock.get(line.product_id.id, 0.0)
        return res

    picking_ids = fields.One2many(
            'stock.picking',
            'analytic_resource_plan_line_id',
            'Pickings', readonly=True)

    qty_fetched = fields.Float(
        string='Fetched Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        default=0.0)
    qty_left = fields.Float(
        string='Quantity left',
        digits=dp.get_precision('Product Unit of Measure'))

    @api.multi
    def _prepare_picking_vals(self):
        self.ensure_one()
        return {
            'origin': self.name,
            'type': 'internal',
            'move_type': 'one',  # direct
            'state': 'draft',
            'date': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            'partner_id': self.account_id.partner_id.id,
            'invoice_state': "none",
            'company_id': self.account_id.company_id.id,
            'location_id': self.account_id.warehouse_id.lot_stock_id.id,
            'location_dest_id': self.account_id.location_id.id,
            'analytic_resource_plan_line_id': self.id,
            'stock_journal_id': 1,
            'note': 'Resource Plan Line %s %s' % (
                self.account_id.id, self.name),
        }

    @api.multi
    def _prepare_move_vals(self, qty_available, picking_id):
        self.ensure_one()
        product_qty = self.unit_amount
        if self.unit_amount > qty_available:
            product_qty = qty_available
        return {
            'name': self.product_id.name_template,
            'priority': '0',
            'date': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            'date_expected': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            'product_id': self.product_id.id,
            'product_qty': product_qty,
            'product_uom': self.product_uom_id.id,
            'partner_id': self.account_id.partner_id.id,
            'picking_id': picking_id,
            'state': 'draft',
            'analytic_account_id': self.account_id.id,
            'price_unit': self.product_id.price,
            'company_id': self.account_id.company_id.id,
            'location_id': self.account_id.warehouse_id.lot_stock_id.id,
            'location_dest_id': self.account_id.location_id.id,
            'note': 'Move for project',
        }


    @api.multi
    def action_button_draft(self):
        res = super(AnalyticResourcePlanLine, self).action_button_draft()
        for line in self:
            if line.picking_ids:
                for picking in line.picking_ids:
                    picking.action_cancel
        return res

    @api.multi
    def action_button_confirm(self):
        for line in self:
            if not line.account_id.warehouse_id:
                raise UserError(
                    _('Could not fetch stock. You have to set a warehouse for'
                      ' the project'))
            elif not line.account_id.warehouse_id.lot_stock_id:
                raise UserError(
                    _('Could not fetch stock. You have to set a stock'
                      ' location for warehouse %s '
                      % line.account_id.warehouse_id.name))
            locations = []
            company_id = line.account_id.company_id.id
            warehouses = self.env['stock.warehouse'].search(
                [('company_id', '=', company_id)])
            for warehouse in warehouses:
                if warehouse.lot_stock_id:
                    locations.append(warehouse.lot_stock_id)
            qty_fetched = 0
            for location in locations:
                if line.qty_fetched < line.unit_amount:
                    qty_available = self._product_available(
                        location.id)[line.id]
                    if qty_available > 0:
                        picking = self._prepare_picking_vals()
                        picking_id = env['stock.picking'].create(picking)
                        move = self._prepare_move_vals(line, qty_available,
                                                       picking_id)
                        qty_fetched += move['product_qty']
                        self.pool.get('stock.move').create(move)
            line.qty_fetched = qty_fetched
            line.qty_left = line.unit_amount - line.qty_fetched
        return super(AnalyticResourcePlanLine, self).action_button_confirm()

    @api.multi
    def unlink(self):
        for line in self:
            if line.picking_ids:
                raise UserError(
                    _('You cannot delete a record that refers to a picking'))
        return super(AnalyticResourcePlanLine, self).unlink()
