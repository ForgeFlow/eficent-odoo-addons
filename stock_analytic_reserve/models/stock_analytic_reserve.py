# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

_STATES = [
    ('draft', 'Draft'),
    ('prepared', 'Prepared'),
    ('confirmed', 'Confirmed'),
    ('done', 'Completed'),
    ('cancel', 'Cancelled')]

_MOVE_STATES = [('draft', 'New'),
                ('cancel', 'Cancelled'),
                ('waiting', 'Waiting Another Move'),
                ('confirmed', 'Waiting Availability'),
                ('assigned', 'Available'),
                ('done', 'Done')]


class StockAnalyticReserve(orm.Model):

    _name = 'stock.analytic.reserve'
    _description = 'Stock Analytic Reservation'

    _columns = {

        'name': fields.char('Reference', required=True),

        'action': fields.selection([('reserve', 'Reserve'),
                                   ('unreserve', 'Unreserve')],
                                   string="Reservation Action",
                                   required=True,
                                   states={'draft': [('readonly', False)]}),

        'state': fields.selection(selection=_STATES,
                                  string='Status',
                                  readonly=True,
                                  required=True,
                                  default='draft',
                                  states={'draft': [('readonly', False)]}),

        'company_id': fields.many2one('res.company', 'Company', required=True),

        'date': fields.date('Date'),

        'warehouse_id': fields.many2one('stock.warehouse', 'Warehouse',
                                        required=True),

        'wh_analytic_reserve_location_id': fields.related(
            'warehouse_id', 'wh_analytic_reserve_location_id',
            type='many2one', relation='stock.location',
            string='Analytic Reservation Location', readonly=True),

        'line_ids': fields.one2many('stock.analytic.reserve.line',
                                    'reserve_id')
    }

    def _get_default_warehouse(self, cr, uid, context=None):
        warehouse_obj = self.pool['stock.warehouse']
        company_id = self.pool.get('res.users').browse(
            cr, uid, uid).company_id.id
        warehouse_ids = warehouse_obj.search(
            cr, uid, [('company_id', '=', company_id)], context=context)
        warehouse_id = warehouse_ids and warehouse_ids[0] or False
        return warehouse_id

    _defaults = {
        'company_id': lambda self, cr, uid, context: self.pool.get(
            'res.users').browse(cr, uid, uid, context).company_id.id,
        'date': fields.date.context_today,
        'state': 'draft',
        'warehouse_id': _get_default_warehouse,
        'name': lambda obj, cr, uid, context: '/'
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool['ir.sequence'].get(
                cr, uid, 'stock.analytic.reserve') or '/'
        return super(StockAnalyticReserve, self).create(cr, uid, vals,
                                                        context=context)

    def action_prepare(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        line_obj = self.pool['stock.analytic.reserve.line']
        for reserve in self.browse(cr, uid, ids, context=context):
            line_ids = [line.id for line in reserve.line_ids]
            line_obj.prepare_stock_moves(cr, uid, line_ids, context=context)
        self.write(cr, uid, ids, {'state': 'prepared'}, context=context)
        return True

    def action_confirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        line_obj = self.pool['stock.analytic.reserve.line']
        for reserve in self.browse(cr, uid, ids, context=context):
            line_ids = [line.id for line in reserve.line_ids]
            line_obj.confirm_stock_moves(cr, uid, line_ids, context=context)
        self.write(cr, uid, ids, {'state': 'confirmed'}, context=context)
        return True

    def action_assign(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        line_obj = self.pool['stock.analytic.reserve.line']
        for reserve in self.browse(cr, uid, ids, context=context):
            line_ids = [line.id for line in reserve.line_ids]
            line_obj.assign_stock_moves(cr, uid, line_ids, context=context)
        return True

    def action_force_assign(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        line_obj = self.pool['stock.analytic.reserve.line']
        for reserve in self.browse(cr, uid, ids, context=context):
            line_ids = [line.id for line in reserve.line_ids]
            line_obj.force_assign_stock_moves(cr, uid, line_ids,
                                              context=context)
        return True

    def action_cancel(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        line_obj = self.pool['stock.analytic.reserve.line']
        for reserve in self.browse(cr, uid, ids, context=context):
            line_ids = [line.id for line in reserve.line_ids]
            line_obj.cancel_stock_moves(cr, uid, line_ids, context=context)
        self.write(cr, uid, ids, {'state': 'cancel'}, context=context)
        return True

    def action_draft(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        line_obj = self.pool['stock.analytic.reserve.line']
        for reserve in self.browse(cr, uid, ids, context=context):
            line_ids = [line.id for line in reserve.line_ids]
            line_obj.remove_stock_moves(cr, uid, line_ids, context=context)
        self.write(cr, uid, ids, {'state': 'draft'}, context=context)
        return True

    def action_done(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        line_obj = self.pool['stock.analytic.reserve.line']
        for reserve in self.browse(cr, uid, ids, context=context):
            line_ids = [line.id for line in reserve.line_ids]
            line_obj.done_stock_moves(cr, uid, line_ids, context=context)
        self.write(cr, uid, ids, {'state': 'done'}, context=context)
        return True

    def copy_data(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}
        default['name'] = '/'
        res = super(StockAnalyticReserve, self).copy_data(
            cr, uid, id, default, context)
        return res


class StockAnalyticReserveLine(orm.Model):

    _name = 'stock.analytic.reserve.line'
    _description = 'Stock Analytic Reservation Line'

    _columns = {
        'reserve_id': fields.many2one('stock.analytic.reserve',
                                      'Stock Analytic Reservation',
                                      required=True,
                                      readonly=True,
                                      ondelete='cascade'),

        'product_id': fields.many2one(
            'product.product', 'Product', required=True,
            domain=[('type', '=', 'product')]),

        'product_uom_qty': fields.float(
            'Quantity',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            required=True),

        'product_uom_id': fields.many2one('product.uom', 'Unit of Measure',
                                          required=True),

        'location_id': fields.many2one('stock.location', 'Stock Location',
                                       required=True),

        'analytic_account_id': fields.many2one('account.analytic.account',
                                               'Analytic Account',
                                               required=True),

        'company_id': fields.related('reserve_id', 'company_id',
                                     type='many2one',
                                     relation='res.company',
                                     string='Company',
                                     store=True, readonly=True),

        'out_move_id': fields.many2one('stock.move', 'Out Stock Move',
                                       readonly=True),

        'out_move_status': fields.related('out_move_id', 'state',
                                          type='selection',
                                          selection=_MOVE_STATES,
                                          string='Out Move Status',
                                          readonly=True),

        'in_move_id': fields.many2one('stock.move', 'In Stock Move',
                                      readonly=True)
    }

    def onchange_product_id(self, cr, uid, ids, product_id, context=None):
        """ Finds UoM for changed product.
        @param product_id: Changed id of product.
        @return: Dictionary of values.
        """
        if product_id:
            prod = self.pool.get('product.product').browse(cr, uid,
                                                           product_id,
                                                           context=context)
            d = {'product_uom_id': [('category_id', '=',
                                     prod.uom_id.category_id.id)]}
            v = {'product_uom_id': prod.uom_id.id}
            return {'value': v, 'domain': d}
        return {'domain': {'product_uom': []}}

    def _prepare_basic_move(self, cr, uid, line, context=None):
        if context is None:
            context = {}

        return {
            'name': line.product_id.name,
            'create_date': fields.datetime.now,
            'date': line.reserve_id.date,
            'product_id': line.product_id.id,
            'product_qty': line.product_uom_qty,
            'product_uom': line.product_uom_id.id,
            'company_id': line.company_id.id,
            'type': 'internal'
        }

    def _prepare_out_move(self, cr, uid, line, context=None):
        res = self._prepare_basic_move(cr, uid, line, context=context)
        res['name'] = _('OUT:') + (line.reserve_id.name or '')
        res['location_id'] = line.location_id.id
        res['location_dest_id'] = \
            line.reserve_id.wh_analytic_reserve_location_id.id
        if line.reserve_id.action == 'unreserve':
            res['analytic_account_id'] = line.analytic_account_id.id
        else:
            res['analytic_account_id'] = False
        return res

    def _prepare_in_move(self, cr, uid, line, context=None):
        res = self._prepare_basic_move(cr, uid, line, context=context)
        res['name'] = _('IN:') + (line.reserve_id.name or '')
        res['location_id'] = line.reserve_id.wh_analytic_reserve_location_id.id
        res['location_dest_id'] = line.location_id.id
        if line.reserve_id.action == 'reserve':
            res['analytic_account_id'] = line.analytic_account_id.id
        else:
            res['analytic_account_id'] = False
        return res

    def prepare_stock_moves(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        move_obj = self.pool['stock.move']
        for line in self.browse(cr, uid, ids, context=context):
            move_out_data = self._prepare_out_move(cr, uid, line,
                                                   context=context)
            out_move_id = move_obj.create(cr, uid, move_out_data,
                                          context=context)
            self.write(cr, uid, [line.id], {'out_move_id': out_move_id},
                       context=context)

            move_in_data = self._prepare_in_move(cr, uid, line,
                                                 context=context)
            in_move_id = move_obj.create(cr, uid, move_in_data,
                                         context=context)
            self.write(cr, uid, [line.id], {'in_move_id': in_move_id},
                       context=context)

        return True

    def confirm_stock_moves(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        move_obj = self.pool['stock.move']
        for line in self.browse(cr, uid, ids, context=context):
            if line.in_move_id.state == 'draft':
                move_obj.action_confirm(cr, uid, [line.in_move_id.id],
                                        context=context)
                move_obj.action_assign(cr, uid, [line.in_move_id.id])

            if line.out_move_id.state == 'draft':
                move_obj.action_confirm(cr, uid, [line.out_move_id.id],
                                        context=context)
                move_obj.action_assign(cr, uid, [line.out_move_id.id])
        return True

    def assign_stock_moves(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        move_obj = self.pool['stock.move']
        for line in self.browse(cr, uid, ids, context=context):
            if line.in_move_id.state not in ['draft', 'cancel', 'done']:
                move_obj.action_assign(cr, uid, [line.in_move_id.id])
            if line.out_move_id.state not in ['draft', 'cancel', 'done']:
                move_obj.action_assign(cr, uid, [line.out_move_id.id])
        return True

    def force_assign_stock_moves(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        move_obj = self.pool['stock.move']
        for line in self.browse(cr, uid, ids, context=context):
            if line.out_move_id.state not in ['draft', 'cancel', 'done']:
                move_obj.force_assign(cr, uid, [line.out_move_id.id],
                                      context=context)
        return True

    def cancel_stock_moves(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        move_obj = self.pool['stock.move']
        for line in self.browse(cr, uid, ids, context=context):
            move_obj.action_cancel(cr, uid, [line.in_move_id.id],
                                   context=context)
            move_obj.action_cancel(cr, uid, [line.out_move_id.id],
                                   context=context)
        return True

    def done_stock_moves(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        move_obj = self.pool['stock.move']
        for line in self.browse(cr, uid, ids, context=context):
            if line.out_move_id.state != 'assigned':
                raise orm.except_orm(_('Error!'),
                                     _('All stock moves must be in status '
                                       'Available.'))
            move_obj.action_done(cr, uid, [line.in_move_id.id],
                                 context=context)
            move_obj.action_done(cr, uid, [line.out_move_id.id],
                                 context=context)
        return True

    def remove_stock_moves(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids,
                   {'out_move_id': False, 'in_move_id': False},
                   context=context)
        return True

    def copy_data(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}
        default['in_move_id'] = False
        default['out_move_id'] = False
        res = super(StockAnalyticReserveLine, self).copy_data(
            cr, uid, id, default, context)
        return res
