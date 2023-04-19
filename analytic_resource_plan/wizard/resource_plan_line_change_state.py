# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.translate import _


class ResourcePlanLineChangeState(models.TransientModel):

    _name = "resource.plan.line.change.state"
    _description = "Change state of resource plan line"

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirm', 'Confirmed')
        ],
        'Status',
        index=True,
        required=True,
        help=' * The \'Draft\' status is used when a user is encoding '
             'a new and unconfirmed resource plan line. '
             '\n* The \'Confirmed\' status is used for to confirm the '
             'resource plan line by the user.'
    )

    @api.multi
    def change_state_confirm(self):
        data = self[0]
        record_ids = self._context and self._context.get('active_ids', False)
        line_plan = self.env['analytic.resource.plan.line'].browse(record_ids)
        new_state = data.state if data and data.state else False
        if new_state == 'draft':
            line_plan.action_button_draft()
        elif new_state == 'confirm':
            line_plan.filtered(
                lambda r: r.parent_id.id is False).action_button_confirm()
        return {
            'domain': "[('id','in', [" + ','.join(
                map(str, record_ids)
            ) + "])]",
            'name': _('Resource Planning Lines'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'analytic.resource.plan.line',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }
