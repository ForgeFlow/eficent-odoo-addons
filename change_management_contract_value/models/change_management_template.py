# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ChangeManagementTemplate(models.Model):
    _name = 'change.management.template'
    _description = 'Change Management Template'

    name = fields.Char('Description', size=256, required=True)
    version_id = fields.Many2one('account.analytic.plan.version',
                                 string='Planning Version', required=True)
    revenue_product_id = fields.Many2one(
        'product.product', string='Revenue product', required=True,)
