# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class AccountAnalyticLinePlan(models.Model):
    _inherit = 'account.analytic.line.plan'

    change_id = fields.Many2one(
        'change.management.change', string='Change Order',
        ondelete='set null')
