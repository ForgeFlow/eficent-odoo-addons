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
from odoo import api, fields, models, _
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DT


class ProgressMeasurementsQuickEntry(models.TransientModel):
    """
    For individual entry of progress measurements
    """
    _name = "progress.measurements.quick.entry"
    _description = "Progress measurements quick entry"

    def _get_default_progress_measurement_type(self):
        meas_type_obj = self.env['progress.measurement.type']
        meas_type = meas_type_obj.search([('is_default', '=', True)],
                                         limit=1)
        return meas_type[0]

    communication_date = fields.Date(
        'Communication date',
        required=True,
        default=datetime.today().strftime(DT)
    )
    progress_measurement_type_id = fields.Many2one(
        'progress.measurement.type',
        'Progress Measurement Type',
        required=True,
        default=_get_default_progress_measurement_type
    )
    value = fields.Float(
        'Measurement value',
        required=True,
        default=0.0
    )

    @api.multi
    def _prepare_measurement_data(self):

        project_obj = self.env['project.project']
        record_id =self._context.get('active_id', False)
        project = project_obj.browse(record_id)
        vals = {
            'project_id': project.id,
            'communication_date': self.communication_date,
            'progress_measurement_type': self.progress_measurement_type_id.id,
            'value': self.value,
        }
        return vals

    def _prepare_measurement_search(self):

        record_id = self._context.get('active_id', False)
        return [('project_id', '=', record_id),
                ('communication_date', '=', self.communication_date),
                ('progress_measurement_type', '=',
                 self.progress_measurement_type_id.id)]

    def progress_measurements_quick_entry_open_window(self):

        meas_obj = self.env['project.progress.measurement']
        meas_vals = self._prepare_measurement_data()
        search_domain = self._prepare_measurement_search()
        del_meas = meas_obj.search(search_domain)
        del_meas.unlink()
        meas_obj.create(meas_vals)
        return True
