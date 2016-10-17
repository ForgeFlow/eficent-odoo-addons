# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, osv
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class project_project(osv.osv):
    
    _inherit = 'project.project'

    def set_done(self, cr, uid, ids, context=None):
        res = super(project_project, self). \
            set_done(cr, uid, ids, context=context)
        projects = self.browse(cr, uid, ids, context)

        for project in projects:
            if project.state == 'close' and not project.date:
                now = datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT)
                self.write(cr, uid, ids, {'date': now}, context=context)
        return res
