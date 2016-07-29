# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# (https://www.eficent.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _


class BusinessRequirementArea(models.Model):
    _name = "business.requirement.area"
    _description = "Business Requirement Area"

    name = fields.Char(string='Name')

