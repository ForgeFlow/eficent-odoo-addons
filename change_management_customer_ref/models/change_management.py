# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ChangeManagementChange(models.Model):
    _inherit = 'change.management.change'

    @api.multi
    @api.depends('project_id')
    def _compute_project_customer(self):
        for change in self:
            change.customer_id = change.project_id.partner_id.id

    def _search_by_project_customer(self, operator, value):
        project_ids = self.env['project.project'].\
            search([('partner_id', operator, value)])
        change_ids = self.env['change.management.change'].\
            search([('project_id', 'in', project_ids.ids)])
        if change_ids:
            return [('id', 'in', change_ids.ids)]
        else:
            return []

    customer_id = fields.Many2one(
        compute='_compute_project_customer',
        search='_search_by_project_customer',
        comodel_name='res.partner',
        string='Customer',
        store=False
    )
    customer_ref = fields.Char(
        string='Customer ref.',
        help="Reference of the Change as indicated by the Customer",
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
