# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm
from openerp.tools.translate import _
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
import time
from openerp import SUPERUSER_ID
import openerp.netsvc as netsvc


class AnalyticResourcePlanLine(orm.Model):

    _inherit = 'analytic.resource.plan.line'

    def _get_product_available(self, cr, uid, ids, location, context=None):

        """ Finds the incoming and outgoing quantity of product on the
        for that analytic account and the location defaulted in the analytic
        account.
        @return: Dictionary of values
        """
        if context is None:
            context = {}
        res = {}
        product_obj = self.pool['product.product']

        for line in self.browse(cr, SUPERUSER_ID, ids, context=context):
            if line.product_id.type == 'service':
                continue
            c = context.copy()
            c.update({'states': ('done',), 'what': ('in', 'out'),
                      'location_id': location})

            stock = product_obj.get_product_available(cr, uid,
                                                      [line.product_id.id],
                                                      context=c)
            res[line.id] = stock.get(line.product_id.id, 0.0)
        return res

    _columns = {
        'picking_ids': fields.one2many(
            'stock.picking',
            'analytic_resource_plan_line_id',
            'Pickings', readonly=True),
    }

    def _prepare_picking_vals(self, cr, uid, line_id, context=None):
        line = self.browse(cr, uid, line_id[0])
        return {
            'origin': line.name,
            'type': 'internal',
            'move_type': 'one',  # direct
            'state': 'draft',
            'date': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            'partner_id': line.account_id.partner_id.id,
            'invoice_state': "none",
            'company_id': line.account_id.company_id.id,
            'location_id': line.account_id.warehouse_id.lot_stock_id.id,
            'location_dest_id': line.account_id.location_id.id,
            'analytic_resource_plan_line_id': line.id,
            'note': 'Resource Plan Line %s %s' % (line.account_id.id, line.name),
        }

    def _prepare_move_vals(self, cr, uid, line, qty_available,
                           picking_id, context=None):
        product_qty = line.unit_amount
        if line.unit_amount > qty_available:
            product_qty = qty_available
        return {
            'name': line.product_id.name_template,
            'priority': '0',
            'date': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            'date_expected': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            'product_id': line.product_id.id,
            'product_qty': product_qty,
            'product_uom': line.product_uom_id.id,
            'partner_id': line.account_id.partner_id.id,
            'picking_id': picking_id,
            'state': 'draft',
            'price_unit': line.product_id.price,
            'company_id': line.account_id.company_id.id,
            'location_id': line.account_id.warehouse_id.lot_stock_id.id,
            'location_dest_id': line.account_id.location_id.id,
            'note': 'RMA move',
        }

    def _prepare_purchase_request_auto(self, cr, uid, line, company_id,
                                       context=None):
        data = {
            'company_id': company_id,
            'origin': line.name,
            'description': line.product_id.name_template,
        }
        return data

    def _prepare_purchase_request_line_auto(self, cr, uid, pr_id, line, qty,
                                            context=None):
        return {
            'request_id': pr_id,
            'name': line.product_id.name,
            'product_qty': qty,
            'product_id': line.product_id.id,
            'product_uom_id': line.product_uom_id.id,
            'date_required': line.date or False,
            'analytic_account_id': line.account_id.id,
            'analytic_resource_plan_lines': [(4, line.id)]
        }

    def _make_auto_purchase_request(
            self, cr, uid, to_purchase, context=None):
        if context is None:
            context = {}
        res = []
        request_obj = self.pool.get('purchase.request')
        request_line_obj = self.pool.get('purchase.request.line')
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
                raise orm.except_orm(
                    _('Could not create purchase request !'),
                    _('You have to select lines '
                      'from the same company.'))
            else:
                company_id = line_company_id

            line_warehouse_id = line.account_id.warehouse_id \
                and line.account_id.warehouse_id.id or False
            if warehouse_id is not False \
                    and line_warehouse_id != warehouse_id:
                raise orm.except_orm(
                    _('Could not create purchase request !'),
                    _('You have to select lines '
                      'from the same warehouse.'))
            else:
                warehouse_id = line_warehouse_id

            if request_id is False:
                request_data = self._prepare_purchase_request_auto(
                    cr, uid, line, company_id,
                    context=context)
                request_id = request_obj.create(cr, uid, request_data, context)
            request_line_data = self._prepare_purchase_request_line_auto(
                cr, uid, request_id, line, qty, context)
            request_line_id = request_line_obj.create(
                cr, uid, request_line_data, context)
            values = {
                'purchase_request_lines': [(4, request_line_id)]
            }
            self.write(cr, uid, [line.id], values, context)
            project_manager_id = line.account_id.user_id and \
                line.account_id.user_id.partner_id.id or False
            if project_manager_id:
                request = request_obj.browse(cr, uid, request_id, context)
                message_follower_ids = [x.id for x in
                                        request.message_follower_ids]
                if project_manager_id not in message_follower_ids:
                    request_obj.write(cr, uid, request_id, {
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

    def action_button_draft(self, cr, uid, ids, context=None):
        res = super(AnalyticResourcePlanLine, self).action_button_draft(
            cr, uid, ids, context=context)
        wf_service = netsvc.LocalService("workflow")
        for line in self.browse(cr, uid, ids, context=context):
            if line.picking_ids:
                for picking in line.picking_ids:
                    wf_service.trg_validate(uid, 'stock.picking', picking.id,
                                            'button_cancel', cr)
        return res

    def action_button_confirm(self, cr, uid, ids, context=None):
        res = super(AnalyticResourcePlanLine, self).action_button_confirm(
            cr, uid, ids, context=context)
        to_purchase = []
        for line in self.browse(cr, uid, ids, context=context):
            if not line.account_id.warehouse_id:
                raise orm.except_orm(
                    _('Could not fetch stock!'),
                    _('You have to set a warehouse for the project'))
            elif not line.account_id.warehouse_id.lot_stock_id:
                raise orm.except_orm(
                    _('Could not fetch stock!'),
                    _('You have to set a stock location for warehouse %s '
                      % line.account_id.warehouse_id.name))
            locations = []
            company_id = line.account_id.company_id.id
            warehouses = self.pool.get('stock.warehouse').search(
                cr, uid, [('company_id', '=', company_id)])
            for warehouse in self.pool.get('stock.warehouse').browse(
                    cr, uid, warehouses, context):
                if warehouse.lot_stock_id:
                    locations.append(warehouse.lot_stock_id)
            qty_fetched = 0
            for location in locations:
                qty_available = self._get_product_available(
                    cr, uid, ids, location, context)[line.id]
                picking = self._prepare_picking_vals(
                    cr, uid, ids, context)
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
        return res

    def unlink(self, cr, uid, ids, context=None):
        for line in self.browse(cr, uid, ids, context=context):
            if line.picking_ids:
                raise orm.except_orm(
                    _('Error!'),
                    _('You cannot delete a record that refers to a picking'))
        return super(AnalyticResourcePlanLine, self).unlink(cr, uid, ids,
                                                            context=context)
