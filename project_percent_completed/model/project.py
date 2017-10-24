# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
#        <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
import time


class Project(models.Model):
    _inherit = "project.project"

    def _compute_poc_on_duration(self):
        res = dict.fromkeys(self._ids, 0.0)
        measurement_type_obj = self.env['progress.measurement.type']
        def_meas_type_ids =\
            measurement_type_obj.search([('is_default', '=', True)])
        if def_meas_type_ids:
            progress_measurement_type =\
                measurement_type_obj.browse(def_meas_type_ids[0].id)
            progress_max_value = progress_measurement_type.default_max_value
        else:
            progress_max_value = 0
        date_today = time.strftime('%Y-%m-%d')

        wbs_projects_data = self._get_project_analytic_wbs()
        # Remove from the list the projects that have been cancelled
        for project_id in wbs_projects_data.keys():
            all_pids = wbs_projects_data[project_id].keys()
            self._cr.execute("""
                WITH progress AS (
                    SELECT p.id as pid,
                    a1.date as date_end,
                    a1.date_start as date_start,
                    COALESCE(abs(a1.date::date - a1.date_start::date), 0) as
                    duration,
                    COALESCE(pm.value, '0') as value,
                    COALESCE(pm.progress_measurement_type, %s) as mt,
                    COALESCE (pm.communication_date, %s) as cdate
                    FROM project_project p
                    INNER JOIN account_analytic_account a1
                    ON a1.id = p.analytic_account_id
                    LEFT OUTER JOIN (
                        SELECT * FROM (
                            SELECT
                                ROW_NUMBER() OVER
                                (PARTITION BY project_id
                                ORDER BY communication_date DESC) AS r,
                                value, project_id, communication_date,
                                progress_measurement_type
                                FROM project_progress_measurement
                                WHERE progress_measurement_type = %s
                                AND project_id in %s
                                AND communication_date <= %s
                        ) x
                        WHERE x.r <= 1
                    ) AS pm ON pm.project_id = p.id
                    WHERE a1.id NOT IN
                    (SELECT parent_id from account_analytic_account a2
                    WHERE a2.parent_id = a1.id)
                    AND p.id in %s
                    -- AND p.state NOT IN ('cancelled', 'pending')
                    ORDER BY p.id
                )
                SELECT DISTINCT(pid) pid, duration, value, cdate,
                date_start, date_end
                FROM progress
                ORDER BY pid, cdate DESC

            """, (def_meas_type_ids[0].id, date_today, def_meas_type_ids[0].id,
                  tuple(all_pids), date_today, tuple(all_pids,)))
            total_dur = 0.0
            ev = 0.0
            for pid, duration, value, cdate, date_start, date_end in \
                    self._cr.fetchall():
                if date_start and date_end:
                    total_dur += duration
                    ev += duration * value / progress_max_value
            if total_dur > 0:
                res[project_id] = round(ev / total_dur * 100)
            else:
                res[project_id] = 0.0
        return res

    poc_rate = fields.Float(
        compute="_compute_poc_on_duration",
        string='% Completed',
        help="""Aggregated percent completed, based on the duration
            of the project"""
    )
