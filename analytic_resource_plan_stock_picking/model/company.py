# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    resource_auto_fetch  = fields.Boolean(
        string='Fetch stock upon RL confirmation',
        readonly=False,
        store=True,
        help='Ony if True the confirmation of RL will try to fetch stock')
