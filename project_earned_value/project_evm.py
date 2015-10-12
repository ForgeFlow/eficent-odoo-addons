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

from openerp.osv import fields, osv


_KPI_TYPE = [('PV', 'Planned Value'),
             ('EV', 'Earned Value'),
             ('AC', 'Actual Cost'),
             ('CV', 'Cost Variance'),
             ('CVP', 'Cost Variance Percent'),
             ('CPI', 'Cost Performance Index'),
             ('TCPI', 'To-Complete Cost Performance Index'),
             ('SV', 'Schedule Variance'),
             ('SVP', 'Schedule Variance Percent'),
             ('SPI', 'Schedule Performance Index'),
             ('EAC', 'Estimate at Completion'),
             ('ETC', 'Estimate to Complete'),
             ('VAC', 'Variance at Completion'),
             ('VACP', 'Variance at Completion Percent'),
             ('BAC', 'Budget at Completion'),
             ('PCC', 'Costs to date / Total costs'),
             ('POC', '% Complete')]


class project_evm(osv.osv):
    """
    EVM

    """
    _name = 'project.evm'
    _description = 'Project Earned Value Management indicators'

    _columns = {
        'name': fields.char('Title', size=64, required=False),
        'date': fields.date('Date'),
        'eval_date': fields.char('Printed Date', size=64, required=True),
        'kpi_type': fields.selection(_KPI_TYPE, 'Type', required=True,),
        'project_id': fields.many2one('project.project', 'Project', ondelete='cascade'),
        'kpi_value': fields.float('Value'),
    }

    def update_all_evm(self, cr, uid, context=None):
        """
        Updates KPI's
        To be used by a scheduled job.
        """
        project_obj = self.pool.get('project.project')

        # Search all the open projects
        project_ids = project_obj.search(cr, uid, [('state', '=', 'open')], context=context)

        project_obj.update_project_evm(cr, uid, project_ids, context=context)
