# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
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


class project(orm.Model):
    _inherit = "project.project"

    def set_done(self, cr, uid, ids, context=None):
        super(project, self).set_done(cr, uid, ids, context=context)
        task_obj = self.pool.get('project.task')
        for proj in self.browse(cr, uid, ids, context=None):
            cr.execute("select id from project_task where project_id=%s "
                       "and state not in ('cancelled','done')", (proj.id,))
            tasks_id = [x[0] for x in cr.fetchall()]
            if tasks_id:
                task_obj.case_close(cr, uid, tasks_id, context=context)
            child_ids = self.search(cr, uid, [('parent_id', '=',
                                               proj.analytic_account_id.id)])
            if child_ids:
                self.set_done(cr, uid, child_ids, context=None)
        return True

    def set_cancel(self, cr, uid, ids, context=None):
        super(project, self).set_cancel(cr, uid, ids, context=context)
        task_obj = self.pool.get('project.task')
        for proj in self.browse(cr, uid, ids, context=None):
            cr.execute("select id from project_task where project_id=%s "
                       "and state not in ('cancelled', 'done')", (proj.id,))
            tasks_id = [x[0] for x in cr.fetchall()]
            if tasks_id:
                task_obj.case_cancel(cr, uid, tasks_id, context=context)
            child_ids = self.search(cr, uid, [('parent_id', '=',
                                               proj.analytic_account_id.id)])
            if child_ids:
                self.set_cancel(cr, uid, child_ids, context=None)
        return True

    def set_pending(self, cr, uid, ids, context=None):
        super(project, self).set_pending(cr, uid, ids, context=context)
        task_obj = self.pool.get('project.task')
        for proj in self.browse(cr, uid, ids, context=None):
            cr.execute("select id from project_task where project_id=%s "
                       "and state not in ('cancelled','done','pending')",
                       (proj.id,))
            tasks_id = [x[0] for x in cr.fetchall()]
            if tasks_id:
                task_obj.case_pending(cr, uid, tasks_id, context=context)
            child_ids = self.search(cr, uid, [('parent_id', '=',
                                               proj.analytic_account_id.id)])
            if child_ids:
                self.set_pending(cr, uid, child_ids, context=None)
        return True

    def set_open(self, cr, uid, ids, context=None):
        super(project, self).set_open(cr, uid, ids, context=context)
        task_obj = self.pool.get('project.task')
        for proj in self.browse(cr, uid, ids, context=None):
            cr.execute("select id from project_task where project_id=%s "
                       "and state in ('cancelled','done')", (proj.id,))
            tasks_id = [x[0] for x in cr.fetchall()]
            if tasks_id:
                task_obj.case_open(cr, uid, tasks_id, context=context)
            child_ids = self.search(cr, uid, [('parent_id', '=',
                                               proj.analytic_account_id.id)])
            if child_ids:
                self.set_open(cr, uid, child_ids, context=None)
        return True
