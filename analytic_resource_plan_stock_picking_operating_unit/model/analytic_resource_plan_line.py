# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, _
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
import time


class AnalyticResourcePlanLine(models.Model):

    _inherit = 'analytic.resource.plan.line'


    @api.multi
    def _prepare_picking_vals(self, warehouse, src_location):
        res = super(AnalyticResourcePlanLine, self)._prepare_picking_vals(
            warehouse, src_location
        )
        res['operating_unit_id'] = self.account_id.location_id.operating_unit_id.id
        return res
