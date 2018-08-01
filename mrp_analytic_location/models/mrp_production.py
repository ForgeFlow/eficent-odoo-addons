# -*- coding: utf-8 -*-
# Copyright 2018 Eficent
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, exceptions, api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.depends('analytic_account_id', 'location_src_id', 'location_dest_id')
    def compute_project_location(self):
        for mnf in self:
            if mnf.analytic_account_id:
                if mnf.analytic_account_id.location_id:
                    mnf.location_src_id = mnf.analytic_account_id.location_id
                    mnf.location_dest_id = mnf.analytic_account_id.location_id
                else:
                    raise exceptions.ValidationError(
                        _('Please create or assign  a location for the '
                          'analytic account'))
        return True

    location_src_id = fields.Many2one(
        compute=compute_project_location, store=True)
    location_dest_id = fields.Many2one(
        compute=compute_project_location, store=True)
