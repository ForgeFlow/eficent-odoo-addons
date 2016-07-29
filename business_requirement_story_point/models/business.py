# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# (https://www.eficent.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _
from openerp.exceptions import except_orm
from openerp import tools
from openerp import SUPERUSER_ID


class BusinessRequirement(models.Model):
    _inherit = "business.requirement"

    story_points = fields.Integer(
        string='Story Points',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
