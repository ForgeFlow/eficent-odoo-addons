# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.model
    def action_produce(self, production_id, production_qty, production_mode,
                       wiz=False):
        production = self.browse(production_id)
        if production_mode == 'consume_produce':
            main_production_move = False
            for produce_product in production.move_created_ids:
                if produce_product.product_id.id == production.product_id.id:
                    main_production_move = produce_product

            total_value = 0.0
            for move in production.move_lines:
                for quant in move.reserved_quant_ids:
                    total_value += quant.cost * quant.qty
            unit_cost = total_value / production.product_qty
            if main_production_move:
                main_production_move.write({'price_unit': unit_cost})
        return super(MrpProduction, self).action_produce(
            production_id, production_qty, production_mode, wiz=wiz)
