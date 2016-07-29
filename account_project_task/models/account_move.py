# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp.tools.translate import _
from openerp import api, fields, models
from openerp.exceptions import Warning


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Task',
        copy=False)
