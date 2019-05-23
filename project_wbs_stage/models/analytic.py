# Copyright 2017-19 Eficent Business and IT Consulting Services S.L.
# Copyright 2017-19 Luxim d.o.o.
# Copyright 2017-19 Matmoz d.o.o.
# Copyright 2017-19 Deneroteam.

# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)..

from odoo import api, models


class AccountAnalyticAccount(models.Model):
    _name = 'account.analytic.account'
    _inherit = ['account.analytic.account', 'base.kanban.abstract']

    @api.multi
    def write(self, values):
        res = super(AccountAnalyticAccount, self).write(values)
        if values.get('stage_id'):
            stage_obj = self.env['base.kanban.stage']
            for aa in self:
                # Search if there's an associated project
                new_stage = stage_obj.browse(values.get('stage_id'))
                # If the new stage is found in the child accounts, then set
                # it as well (only if the new stage sequence is greater than
                #  the current)
                child_ids = self.search([('parent_id', '=', aa.id)])
                for child in child_ids:
                    if child.stage_id.sequence < new_stage.sequence:
                        child.write({'stage_id': new_stage.id})
            for project in self.project_ids:
                project.write({'stage_id': values.get('stage_id')})
        return res
