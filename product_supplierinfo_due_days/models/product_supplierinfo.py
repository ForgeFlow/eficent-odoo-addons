# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models
import datetime

class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    due_days = fields.Integer(
        string='Days due to expire',
        search='_search_due_days',
        compute='_compute_due_days'
    )

    def _search_due_days(self, operator, value):
        due_date = fields.Date.from_string(fields.Date.today()) + \
                   datetime.timedelta(days=value)
        if operator in ('!=', '<>'):
            raise ValueError('Invalid operator: %s' % (operator,))
        return [('date_end', operator, due_date)]

    @api.depends('date_end')
    def _compute_due_days(self):
        today_date = fields.Date.from_string(fields.Date.today())
        for rec in self:
            rec.due_days = 0
            date_end = fields.Date.from_string(rec.date_end)
            if rec.date_end:
                due_days = (date_end - today_date).days
                if due_days >= 0:
                    rec.due_days = due_days
