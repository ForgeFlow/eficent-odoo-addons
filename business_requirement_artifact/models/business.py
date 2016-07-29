# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# (https://www.eficent.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _


class BusinessRequirement(models.Model):
    _inherit = "business.requirement"

    artifact_id = fields.Many2one(
        comodel_name='business.requirement.artifact',
        string='Artifact',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
