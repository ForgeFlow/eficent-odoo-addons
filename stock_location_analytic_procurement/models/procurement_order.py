# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, _


class ProcurementOrder(models.Model):
    _inherit = "procurement.order"

    @api.model
    def _search_suitable_rule(self, domain):
        """
        Removing the rules with wrong picking type
        """
        res = super(ProcurementOrder, self)._search_suitable_rule(domain)
        res_filtered = res.filtered(
            lambda rule: rule.picking_type_id.default_location_src_id.
            analytic_account_id == self.account_analytic_id or
            self.location_id.analytic_account_id == self.account_analytic_id)
        if res and not res_filtered:
            self.message_post(body=_('''Either the procurement location
                does not belong to the analytic account or no destination
                location for that analytic account found in the rule.'''))
        return res_filtered
