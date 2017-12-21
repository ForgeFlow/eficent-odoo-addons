# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Project(models.Model):
    _inherit = 'project.project'

    cost_category = fields.Selection(
        [('cogs', 'Cost of Goods Sold'),
         ('expense', 'Expense')],
        string='Type of Cost',
        help="""Defines what type of cost does the analytic account carry
        from an employee perspective.""",
        default='cogs'
    )
