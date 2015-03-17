# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent (<http://www.eficent.com/>)
#               <contact@eficent.com>
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
from datetime import datetime, date, timedelta


class project(orm.Model):
    _inherit = "project.project"

    def _compute_poc_on_duration(self, cr, uid, ids, names,
                                            arg, context=None):
        res = {}
        if context is None:
            context = {}

        measurement_type_obj = self.pool.get('progress.measurement.type')
        project_obj = self.pool.get('project.project')
        def_meas_type_ids = measurement_type_obj.search(
            cr, uid, [('is_default', '=', True)], context=context)

        if def_meas_type_ids:
            progress_measurement_type = measurement_type_obj.browse(
                cr, uid, def_meas_type_ids[0], context=context)
            progress_max_value = progress_measurement_type.default_max_value
        else:
            progress_max_value = 0

        date_today = time.strftime('%Y-%m-%d')
        # Search for child projects
        wbs_projects_data = project_obj._get_project_analytic_wbs(
            cr, uid, ids, context=context)

        for proj in self.browse(cr, uid, wbs_projects_data.keys(),
                                context=context):
            total_duration = {}
            for wbs_project in self.browse(cr, uid, wbs_projects_data[
                proj.id].keys(), context=context):
                if wbs_project.date_start and wbs_project.date:
                    date_start = datetime.strptime(wbs_project.date_start, "%Y-%m-%d")
                    date_end = datetime.strptime(wbs_project.date, "%Y-%m-%d")
                    d = date_start - date_end
                    d_days = d.days
                    total_duration[wbs_project.id] = abs(d_days)
                else:
                    total_duration[wbs_project.id] = 0
            tot_dur = sum(total_duration.values())
            ev = 0.0
            for wbs_project_id in wbs_projects_data[proj.id].keys():

                cr.execute('SELECT DISTINCT ON (a.project_id) value '
                           'FROM project_progress_measurement AS a '
                           'WHERE a.project_id IN %s '
                           'AND a.progress_measurement_type = %s '
                           'AND a.communication_date <= %s '
                           'ORDER BY a.project_id, '
                           'a.communication_date DESC ',
                           (tuple([wbs_project_id]),
                            def_meas_type_ids[0],
                            date_today))
                cr_result = cr.fetchone()
                measurement_value = cr_result and cr_result[0] or 0.0
                ev += total_duration[wbs_project_id] * measurement_value / \
                    progress_max_value
            if tot_dur > 0:
                res[proj.id] = round(ev / tot_dur * 100, 2)
            else:
                res[proj.id] = 0.0
        return res

    _columns = {
        'progress_rate': fields.function(_compute_poc_on_duration,
                                         method=True, string='% Completed',
                                         type='float',
                                         help="""Aggregated percent
                                         completed, based on the duration
                                         of the project
                                       """),
    }