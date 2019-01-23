# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, orm


class AccountAnalyticLinePlan(orm.Model):
    _inherit = 'account.analytic.line.plan'

    _columns = {
        'change_id': fields.many2one(
            'change.management.change', 'Change Order',
            ondelete='set null')
    }
