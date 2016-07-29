# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models


class ProcurementOrder(models.Model):
    _inherit = "procurement.order"

    @api.model
    def _run_move_create(self, procurement):
        vals = super(ProcurementOrder, self)._run_move_create(procurement)
        if procurement.project_id:
            vals['project_id'] = procurement.project_id.id
        return vals
