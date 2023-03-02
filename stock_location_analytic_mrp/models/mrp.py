# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, exceptions, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.multi
    @api.constrains("operating_unit_id", "location_src_id", "location_dest_id")
    def _check_mrp_analytic_location(self):
        for mrp in self:
            if mrp.analytic_account_id:
                analytic = mrp.analytic_account_id
                if (
                    mrp.location_src_id.analytic_account_id != analytic
                    or mrp.location_dest_id.analytic_account_id != analytic
                ):
                    raise exceptions.ValidationError(
                        _(
                            "The production location does not belong to the "
                            "analytic account"
                        )
                    )

    def _generate_raw_move(self, bom_line, line_data):
        """WARNING! OVERRIDE ODOO, WILL NOT DO A HOOK FOR THIS"""
        quantity = line_data["qty"]
        # alt_op needed for the case when you explode phantom bom and all the lines will be consumed in the operation given by the parent bom line
        alt_op = (
            line_data["parent_line"]
            and line_data["parent_line"].operation_id.id
            or False
        )
        if bom_line.child_bom_id and bom_line.child_bom_id.type == "phantom":
            return self.env["stock.move"]
        if bom_line.product_id.type not in ["product", "consu"]:
            return self.env["stock.move"]
        if self.routing_id:
            routing = self.routing_id
        else:
            routing = self.bom_id.routing_id
        if routing and routing.location_id:
            source_location = routing.location_id
        else:
            source_location = self.location_src_id
        original_quantity = (self.product_qty - self.qty_produced) or 1.0
        data = {
            "sequence": bom_line.sequence,
            "name": self.name,
            "date": self.date_planned_start,
            "date_expected": self.date_planned_start,
            "bom_line_id": bom_line.id,
            "product_id": bom_line.product_id.id,
            "product_uom_qty": quantity,
            "product_uom": bom_line.product_uom_id.id,
            "location_id": source_location.id,
            "location_dest_id": self.product_id.property_stock_production.id,
            "raw_material_production_id": self.id,
            "company_id": self.company_id.id,
            "operation_id": bom_line.operation_id.id or alt_op,
            "price_unit": bom_line.product_id.standard_price,
            "procure_method": "make_to_stock",
            "origin": self.name,
            "warehouse_id": source_location.get_warehouse().id,
            "group_id": self.procurement_group_id.id,
            "propagate": self.propagate,
            "unit_factor": quantity / original_quantity,
            "analytic_account_id": self.analytic_account_id.id,
        }
        return self.env["stock.move"].create(data)

    def _generate_finished_moves(self):
        """WARNING! OVERRIDE ODOO, WILL NOT DO A HOOK FOR THIS"""
        move = self.env["stock.move"].create(
            {
                "name": self.name,
                "date": self.date_planned_start,
                "date_expected": self.date_planned_start,
                "product_id": self.product_id.id,
                "product_uom": self.product_uom_id.id,
                "product_uom_qty": self.product_qty,
                "location_id": self.product_id.property_stock_production.id,
                "location_dest_id": self.location_dest_id.id,
                "move_dest_id": self.procurement_ids
                and self.procurement_ids[0].move_dest_id.id
                or False,
                "procurement_id": self.procurement_ids
                and self.procurement_ids[0].id
                or False,
                "company_id": self.company_id.id,
                "production_id": self.id,
                "origin": self.name,
                "group_id": self.procurement_group_id.id,
                "propagate": self.propagate,
                "analytic_account_id": self.analytic_account_id.id,
            }
        )
        move.action_confirm()
        return move
