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
from openerp.osv import orm, fields
import time


class ProgressMeasurementsQuickEntry(orm.TransientModel):
    """
    For individual entry of progress measurements
    """
    _name = "progress.measurements.quick.entry"
    _description = "Progress measurements quick entry"

    def _get_default_progress_measurement_type(self, cr, uid, context=None):
        meas_type_obj = self.pool['progress.measurement.type']
        meas_type = meas_type_obj.search(cr, uid, [('is_default', '=', True)],
                                         limit=1)
        return meas_type[0]

    _columns = {
        'communication_date': fields.date('Communication date',
                                          required=True),
        'progress_measurement_type_id': fields.many2one(
            'progress.measurement.type', 'Progress Measurement Type',
            required=True),
        'value': fields.float('Measurement value', required=True),
    }

    _defaults = {
        'communication_date': time.strftime('%Y-%m-%d'),
        'progress_measurement_type_id': _get_default_progress_measurement_type,
        'value': 100,
    }

    def _prepare_measurement_data(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        project_obj = self.pool.get('project.project')
        record_id = context and context.get('active_id', False)
        project = project_obj.browse(cr, uid, record_id, context=context)
        data = self.browse(cr, uid, ids, context=context)[0]
        communication_date = data.communication_date
        vals = {
            'project_id': project.id,
            'communication_date': communication_date,
            'progress_measurement_type': data.progress_measurement_type_id.id,
            'value': data.value,
        }
        return vals

    def progress_measurements_quick_entry_open_window(self, cr, uid, ids,
                                                      context=None):
        if context is None:
            context = {}
        meas_obj = self.pool.get('project.progress.measurement')
        meas_vals = self._prepare_measurement_data(cr, uid, ids,
                                                   context=context)
        meas_obj.create(cr, uid, meas_vals, context=context)
        return True
