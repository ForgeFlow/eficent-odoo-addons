# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, _
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import ValidationError
import odoo.addons.decimal_precision as dp
import time


class AnalyticResourcePlanLine(models.Model):
    _inherit = "analytic.resource.plan.line"

    @api.multi
    @api.depends("picking_ids", "picking_ids.state")
    def _compute_qty_fetched(self):
        qty = 0.0
        for line in self:
            for picking in line.picking_ids.filtered(
                lambda p: p.state != "cancel"
            ):
                for move in picking.move_lines:
                    qty += move.product_uom_qty
            line.qty_fetched = qty

    @api.multi
    @api.depends("picking_ids", "picking_ids.state")
    def _compute_qty_left(self):
        qty = 0.0
        for line in self:
            for picking in line.picking_ids.filtered(
                lambda p: p.state != "cancel"
            ):
                for move in picking.move_lines:
                    qty += move.product_uom_qty
            line.qty_left = line.unit_amount - qty

    picking_ids = fields.One2many(
        "stock.picking",
        "analytic_resource_plan_line_id",
        "Pickings",
        readonly=True,
    )
    qty_fetched = fields.Float(
        string="Fetched Quantity",
        digits=dp.get_precision("Product Unit of Measure"),
        compute=_compute_qty_fetched,
    )
    qty_left = fields.Float(
        string="Quantity left",
        default=lambda self: self.unit_amount,
        compute=_compute_qty_left,
        digits=dp.get_precision("Product Unit of Measure"),
    )

    @api.multi
    def _prepare_picking_vals(self, src_location_id):
        self.ensure_one()
        dest_location = self.account_id.location_id

        picking_type_id = self.env["stock.picking.type"].search(
            [
                ("code", "=", "incoming"),
                (
                    "warehouse_id.company_id",
                    "=",
                    self.account_id.company_id.id,
                ),
            ], limit=1
        )
        if not picking_type_id:
            raise ValidationError(
                _("No valid picking type for the projects location")
            )
        return {
            "origin": self.name,
            "move_type": "one",  # direct
            "state": "draft",
            "picking_type_id": picking_type_id.id,
            "date": time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            "partner_id": self.account_id.partner_id.id,
            "company_id": self.account_id.company_id.id,
            "location_id": src_location_id.id,
            "location_dest_id": dest_location.id,
            "analytic_resource_plan_line_id": self.id,
            "note": "Resource Plan Line %s %s"
            % (self.account_id.id, self.name),
        }

    @api.multi
    def _prepare_move_vals(self, qty, picking_id, scr_location):
        self.ensure_one()
        return {
            "name": self.product_id.product_tmpl_id.name,
            "priority": "0",
            "date": time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            "date_expected": time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            "product_id": self.product_id.id,
            "product_uom_qty": qty,
            "product_uom": self.product_uom_id.id,
            "partner_id": self.account_id.partner_id.id,
            "picking_id": picking_id.id,
            "state": "draft",
            "analytic_account_id": self.account_id.id,
            "price_unit": self.product_id.standard_price,
            "company_id": self.account_id.company_id.id,
            "location_id": scr_location.id,
            "location_dest_id": self.account_id.location_id.id,
            "note": "Move for project",
        }

    @api.multi
    def action_button_draft(self):
        res = super(AnalyticResourcePlanLine, self).action_button_draft()
        for line in self:
            if line.picking_ids:
                for picking in line.picking_ids:
                    picking.action_cancel()
        return res

    @api.multi
    def action_button_confirm(self):
        for line in self:
            if line.child_ids:
                continue
            if not line.account_id.location_id:
                raise ValidationError(
                    _("Could not fetch stock. "
                      "You have to set a location for the project")
                )
            company_id = line.account_id.company_id.id
            warehouses = self.env["stock.warehouse"].search(
                [("company_id", "=", company_id)]
            )
            qty_fetched = line.qty_fetched
            for warehouse in warehouses:
                if warehouse.lot_stock_id:
                    get_sublocations = self.env["stock.location"].search(
                        [
                            ("id", "child_of", warehouse.lot_stock_id.ids),
                            ("analytic_account_id", "=", False),
                        ]
                    )
                    for location_id in get_sublocations:
                        if qty_fetched < line.unit_amount:
                            stock = line.with_context(
                                location=location_id.id
                            ).product_id._product_available()
                            qty_available = stock[line.product_id.id][
                                "qty_available"
                            ]
                            if qty_available > 0:
                                picking = self._prepare_picking_vals(
                                    location_id
                                )
                                picking_id = self.env[
                                    "stock.picking"
                                ].create(picking)
                                if qty_available > line.unit_amount:
                                    qty_to_fetch = line.unit_amount
                                else:
                                    qty_to_fetch = qty_available
                                move_vals = line._prepare_move_vals(
                                    qty_to_fetch, picking_id, location_id
                                )
                                move = self.env["stock.move"].create(
                                    move_vals
                                )
                                qty_fetched += move.product_uom_qty
            return super(
                AnalyticResourcePlanLine, self
            ).action_button_confirm()
        return super(AnalyticResourcePlanLine, self).action_button_confirm()

    @api.multi
    def unlink(self):
        for line in self:
            if line.picking_ids:
                raise ValidationError(
                    _("You cannot delete a record that refers to a picking")
                )
        return super(AnalyticResourcePlanLine, self).unlink()
