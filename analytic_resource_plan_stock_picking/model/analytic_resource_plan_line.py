# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models, _
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import UserError
import time
from openerp import SUPERUSER_ID
import openerp.netsvc as netsvc


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
    def _prepare_purchase_request_auto(self, company_id):
        self.ensure_one()
        data = {
            'company_id': company_id,
            'origin': self.name,
            'description': self.product_id.name_template,
        }
        return data

    @api.multi
    def _prepare_purchase_request_line_auto(self, pr_id, qty):
        self.ensure_one()
        return {
            'request_id': pr_id,
            'name': self.product_id.name,
            'product_qty': qty,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom_id.id,
            'date_required': self.date or False,
            'analytic_account_id': self.account_id.id,
            'analytic_resource_plan_lines': [(4, self.id)]
        }

    @api.model
    def _make_auto_purchase_request(self, to_purchase):
        res = []
        request_obj = self.en['purchase.request']
        request_line_obj = self.env['purchase.request.line']
        company_id = False
        warehouse_id = False
        request_id = False
        for item in to_purchase:
            line = item[0]
            qty = item[1]
            line_company_id = line.account_id.company_id \
                and line.account_id.company_id.id or False
            if company_id is not False \
                    and line_company_id != company_id:
                raise UserError(
                    _('Could not create purchase request. You have to select'
                      ' lines from the same company.'))
            else:
                company_id = line_company_id

            line_warehouse_id = line.account_id.warehouse_id \
                and line.account_id.warehouse_id.id or False
            if warehouse_id is not False \
                    and line_warehouse_id != warehouse_id:
                raise UserError(
                    _('Could not create purchase request. You have to select'
                      ' lines from the same warehouse.'))
            else:
                warehouse_id = line_warehouse_id

            if request_id is False:
                request_data = self._prepare_purchase_request_auto(
                    line, company_id)
                request_id = request_obj.create(request_data)
            request_line_data = self._prepare_purchase_request_line_auto(
                request_id, line, qty)
            request_line_id = request_line_obj.create(
                request_line_data)
            values = {
                'purchase_request_lines': [(4, request_line_id)]
            }
            self.write([line.id], values)
            project_manager_id = line.account_id.user_id and \
                line.account_id.user_id.partner_id.id or False
            if project_manager_id:
                request = request_obj.browse(request_id)
                message_follower_ids = [x.id for x in
                                        request.message_follower_ids]
                if project_manager_id not in message_follower_ids:
                    request_obj.write(request_id, {
                        'message_follower_ids': (4, project_manager_id)})
            res.append(request_line_id)

        return {
            'domain': "[('id','in', ["+','.join(map(str, res))+"])]",
            'name': _('Purchase Request Lines'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.request.line',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }

    @api.multi
    def action_button_draft(self):
        res = super(AnalyticResourcePlanLine, self).action_button_draft()
        wf_service = netsvc.LocalService("workflow")
        for line in self.browse(cr, uid, ids, context=context):
            if line.picking_ids:
                for picking in line.picking_ids:
                    wf_service.trg_validate(uid, 'stock.picking', picking.id,
                                            'button_cancel', cr)
        return res

    @api.multi
    def action_button_confirm(self):
        to_purchase = []
        for line in self:
            if not line.account_id.warehouse_id:
                raise UserError(
                    _('Could not fetch stock. You have to set a warehouse for'
                      ' the project'))
            elif not line.account_id.warehouse_id.lot_stock_id:
                raise orm.except_orm(
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
                    # locations = list(set(locations))

            # locations_ids = []
            # for loc in locations:
            #     locations_ids.append(loc.id)
            # child_location_ids = self.pool.get('stock.location').search(cr, uid, [
            #     ('location_id', 'child_of', locations_ids)])
            # locations = self.pool.get('stock.location').search(cr, uid, [
            #     ('name', 'like', 'Stock')])
            qty_fetched = 0
            for location in locations:
                if qty_fetched < line.unit_amount:
                    qty_available = self._product_available(
                        location.id)[line.id]
                    if qty_available > 0:
                        picking = self._prepare_picking_vals()
                        picking_id = self.pool.get('stock.picking').create(
                            cr, uid, picking)
                        move = self._prepare_move_vals(
                            cr, uid, line, qty_available, picking_id, context)
                        qty_fetched += move['product_qty']
                        self.pool.get('stock.move').create(cr, uid, move)

            qty_left = line.unit_amount - qty_fetched
            if qty_left > 0:
                to_purchase.append((line, qty_left))
            if len(to_purchase) > 0:
                self._make_auto_purchase_request(cr, uid, to_purchase,
                                                 context)
        return super(AnalyticResourcePlanLine, self).action_button_confirm(
            cr, uid, ids, context=context)

    @api.multi
    def unlink(self):
        for line in self:
            if line.picking_ids:
                raise UserError(
                    _('You cannot delete a record that refers to a picking'))
        return super(AnalyticResourcePlanLine, self).unlink()
