# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, orm
from openerp.tools.translate import _


class LocationAnalyticCreate(orm.TransientModel):
    _name = 'location.analytic.create'
    _description = 'Create an analytic Location'

    def _prepare_location(self, cr, uid, wizard, context=None):
        if context is None:
            context = {}
        return {
            'name': wizard.name,
            'location_id': wizard.location_id.id,
            'type': 'internal' if wizard.type == 'internal' else 'customer',
            'analytic_account_id': context['default_analytic_account_id'],
        }

    def create_location(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = []
        wizard = self.browse(cr, uid, ids[0], context=context)
        loc_obj = self.pool.get('stock.location')
        loc_data = self._prepare_location(
            cr, uid, wizard, context=context)

        new_loc = loc_obj.create(
            cr, uid, loc_data, context=context)

        res.append(new_loc)

        return {
            'domain': "[('id','in', ["+','.join(map(str, res))+"])]",
            'name': _('Locations for projects'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.location',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }

    def _get_analytic_locations(self, cr, uid, ids, context=None):
        if context is None:
            return
        if 'default_analytic_account_id' not in context:
            return
        res = {}
        analytic_id = context['default_analytic_account_id']
        location_ids = self.pool.get('stock.location').search(
            cr, uid, ['analytic_account_id', '=', analytic_id])
        ch_location_ids = self.pool.get('stock.location')._get_sublocations(
            cr, uid, location_ids)
        for wiz_id in self.browse(cr, uid, ids, context=context):
            res[wiz_id] = []
            for loc in ch_location_ids:
                res[wiz_id].appenf(loc.id)
        return res

    _columns = {
        'name': fields.char('Description', size=256, required=True),
        'location_id': fields.many2one('stock.location', 'Parent location',
                                       required=False,
                                       domain="[('usage', '=', type)]"),
        'type': fields.selection([('internal', 'Internal'),
                                  ('customer', 'External')],
                                 'Type', required=True),
    }


class AnalyticocationManager(orm.TransientModel):
    _name = 'analytic.location.manager'
    _description = 'Manage analytic Locations'

    _columns = {
        'recursive': fields.boolean("Include Sublocations"),
    }
    def open_location_manager(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        return {'type': 'ir.actions.act_window',
                'name': 'Create Location For Project',
                'res_model': 'location.analytic.create',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'context': context,
                }

    def show_analytic_locations(self, cr, uid, ids, context=None):
        if context is None:
            return
        if 'default_analytic_account_id' not in context:
            return
        analytic_id = context['default_analytic_account_id']
        location_ids = self.pool.get('stock.location').search(
            cr, uid, [('analytic_account_id', '=', analytic_id)])
        for wiz_id in self.browse(cr, uid, ids, context=context):
            if wiz_id.recursive:
                ch_location_ids = self.pool.get(
                    'stock.location')._get_sublocations(
                    cr, uid, location_ids)
                location_ids.extend(ch_location_ids)
            res = list(set(location_ids))

        return {'type': 'ir.actions.act_window',
                'name': _('Locations for project'),
                'res_model': 'stock.location',
                'view_type': 'form',
                'view_mode': 'tree, form',
                'target': 'current',
                'domain': [('id', 'in', res)],
                'nodestroy': True,
                }

