# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm
from openerp.tools.translate import _


class project_change_state(orm.TransientModel):
    """
    This wizard will confirm the all the selected draft invoices
    """

    _name = "project.change.state"
    _description = "Change the status of the selected invoices"

    def set_pending(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        project_obj = self.pool.get('project.project')
        for project in project_obj.browse(cr, uid, context['active_ids'],
                                          context=context):
            if project.state != 'open':
                raise orm.except_orm(_('Warning!'),
                                     _("Selected project(s) cannot be "
                                       "changed to 'Pending' state as they "
                                       "are not all in 'Open' state."))
            project_obj.set_pending(cr, uid, [project.id], context=context)

        return {'type': 'ir.actions.act_window_close'}

    def set_open(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        project_obj = self.pool.get('project.project')
        for project in project_obj.browse(cr, uid, context['active_ids'],
                                          context=context):
            if project.state not in ('pending', 'close', 'cancelled'):
                raise orm.except_orm(_('Warning!'),
                                     _("Selected project(s) cannot be "
                                       "changed to 'Open' state as they "
                                       "are not all in 'Pending', "
                                       "'Closed' or 'Cancelled' states."))
            project_obj.set_open(cr, uid, [project.id], context=context)

        return {'type': 'ir.actions.act_window_close'}

    def set_done(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        project_obj = self.pool.get('project.project')
        for project in project_obj.browse(cr, uid, context['active_ids'],
                                          context=context):
            if project.state not in ('open', 'pending'):
                raise orm.except_orm(_('Warning!'),
                                     _("Selected project(s) cannot be "
                                       "changed to 'Done' state as they "
                                       "are not all in 'Pending' or 'Open' "
                                       "states."))
            project_obj.set_done(cr, uid, [project.id], context=context)

        return {'type': 'ir.actions.act_window_close'}

    def set_cancel(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        project_obj = self.pool.get('project.project')
        for project in project_obj.browse(cr, uid, context['active_ids'],
                                          context=context):
            if project.state not in ('open', 'pending', 'close'):
                raise orm.except_orm(_('Warning!'),
                                     _("Selected project(s) cannot be "
                                       "changed to 'Cancelled' state as they "
                                       "are not all in 'Pending', 'Open' "
                                       "or 'Done' states."))
            project_obj.set_cancel(cr, uid, [project.id], context=context)

        return {'type': 'ir.actions.act_window_close'}
