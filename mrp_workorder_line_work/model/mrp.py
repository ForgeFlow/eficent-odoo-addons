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
from openerp.osv import fields, orm
import time
from openerp import tools
import datetime


class mrp_production_workcenter_line(orm.Model):
    _inherit = 'mrp.production.workcenter.line'

    _columns = {
        'company_id': fields.related('workcenter_id', 'company_id',
                                     type='many2one', relation='res.company',
                                     string='Company', store=True,
                                     readonly=True),
        'work_ids': fields.one2many('mrp.production.workcenter.line.work',
                                    'workcenter_line_id', 'Work done'),
    }


class mrp_production_workcenter_line_work(orm.Model):
    _name = "mrp.production.workcenter.line.work"
    _description = "Work Center Line Work"
    _columns = {
        'name': fields.char('Work summary', size=128),
        'date': fields.datetime('Date', select="1"),
        'workcenter_line_id': fields.many2one(
            'mrp.production.workcenter.line', 'Workcenter line',
            ondelete='cascade', required=True, select="1"),
        'hours': fields.float('Time Spent'),
        'user_id': fields.many2one('res.users', 'Done by',
                                   required=True, select="1"),
        'company_id': fields.related('workcenter_line_id', 'company_id',
                                     type='many2one', relation='res.company',
                                     string='Company', store=True,
                                     readonly=True)
    }

    _defaults = {
        'user_id': lambda obj, cr, uid, context: uid,
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S')
    }

    _order = "date desc"
