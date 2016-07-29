# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models
from openerp.tools.translate import _
from openerp.exceptions import UserError


class Project(models.Model):
    _inherit = 'project.project'

    displayed_image_id = fields.Many2one(
        comodel_name='ir.attachment',
        string='Displayed Image',
        domain="[('res_model', '=', 'project.project'), "
               "('res_id', '=', id), ('mimetype', 'ilike', 'image')]"

    )
