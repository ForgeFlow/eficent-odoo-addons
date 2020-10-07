# -*- coding: utf-8 -*-

from odoo import models, fields


class StockConfigSettings(models.TransientModel):
    _inherit = 'stock.config.settings'
    
    resource_auto_request  = fields.Boolean(
        related='company_id.resource_auto_request')
