# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, orm


class AnalyticAccountStage(orm.Model):
    _inherit = 'analytic.account.stage'

    _columns = {
        'use_timesheets': fields.boolean(
            'Timesheets',
            help="Check this field if setting this stage should make the  "
                 "project to manage timesheets"),
    }

    _defaults = {
        'use_timesheets': True
    }
