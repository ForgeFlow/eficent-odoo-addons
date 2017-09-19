# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ChangeManagementChange(models.Model):
    _inherit = 'change.management.change'

    def _get_change_orders_project(self, cr, uid, ids, context=None):
        result = set()
        project_obj = self.env['project.project']
        for order in project_obj.browse(cr, uid, ids, context=context):
            for change in order.change_ids:
                result.add(change.id)
        return list(result)

    @api.multi
    @api.depends('project_id')
    def _get_project_customer(self):
        for change in self:
            change.customer_id = change.project_id.partner_id.id

    def _search_by_project_customer(self, operator, value):
        project_ids = self.env['project.project'].\
            search([('partner_id', operator, value)])
        change_ids = self.env['change.management.change'].\
            search([('project_id', 'in', project_ids.ids)])
        if change_ids:
            return [('id', 'in', tuple(change_ids.ids))]
        else:
            return []

    customer_id = fields.Many2one(
        compute='_get_project_customer',
        search='_search_by_project_customer',
        comodel_name='res.partner',
        string='Customer',
        readonly=True,
        store=False
    )
    customer_ref = fields.Char(
        'Customer ref.',
        help="Reference of the Change as indicated by the Customer",
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
