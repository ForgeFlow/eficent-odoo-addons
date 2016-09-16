# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class ProductProduct(models.Model):

    _inherit = "product.product"

    @api.multi
    def internal_transfer(self):
        "Creates a picking of internal transfer for the product."
        self.ensure_one()
        picking_obj = self.env['stock.picking']
        type_obj = self.env['stock.picking.type']
        user_obj = self.env['res.users']
        move_obj = self.env['stock.move']
        company_id = user_obj.browse(self._uid).company_id.id
        types = type_obj.search([('code', '=', 'internal'),
                                 ('warehouse_id.company_id', '=', company_id)])
        if not types:
            raise UserError(_("Make sure you have at least an internal picking"
                              "type defined for your company's warehouse."))
        picking_type = types[0]
        # on_change for product
        new_line = move_obj.new()
        res = new_line.onchange_product_id(prod_id=self.id)
        # on_change for picking type
        new_line = picking_obj.new()
        vals = new_line.onchange_picking_type(picking_type_id=picking_type.id,
                                              partner_id=False)
        picking = picking_obj.create({
            'picking_type_id': picking_type.id,
            'location_dest_id': vals.get('value').get('location_dest_id'),
            'location_id': vals.get('value').get('location_id'),
            'picking_type_code': vals.get('value').get('picking_type_code'),
            'move_lines': [(0, 0, {
                'name': res.get('value').get('name'),
                'product_id': self.id,
                'product_uom_qty': res.get('value').get('product_uom_qty'),
                'product_uom': res.get('value').get('product_uom'),
                'state': 'draft',
            })]
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stock Picking',
            'res_model': 'stock.picking',
            'res_id': picking.id,
            'view_mode': 'form',
            'view_type': 'form',
        }
