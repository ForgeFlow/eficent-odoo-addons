# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    resource_auto_request  = fields.Boolean(
        string='Create Purchase Request upon RL confirmation',
        readonly=False,
        store=True,
        help='Ony if True the confirmation of RL will generate a Purchase Request')
