# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models
from openerp.exceptions import ValidationError, Warning
from openerp.tools.translate import _


class PartnerExternalReference(models.Model):
    _name = "partner.external.reference"
    _description = "Partner External Reference"

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=True
    )
    name = fields.Char('External Reference', required=True)
    origin_id = fields.Many2one(
        comodel_name='partner.external.reference.origin',
        string='Origin',
        required=True
    )
