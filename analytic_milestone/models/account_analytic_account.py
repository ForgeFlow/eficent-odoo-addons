# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    milestone_ids = fields.One2many(
        'analytic.milestone',
        'account_id',
        string="Milestones"
    )
    milestone_product_id = fields.Many2one(
        'product.product',
        string="Default Product used when invoicing milestones")
