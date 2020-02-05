# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    @api.model
    def get_parent_stock_data(self):
        context = self.env.context
        res = {}
        if "default_parent_id" in context and context["default_parent_id"]:
            for project in self.search(
                [("analytic_account_id", "=", context["default_parent_id"])],
                limit=1,
            ):
                res["location_id"] = project.location_id
                res["dest_address_id"] = project.dest_address_id
        return res

    @api.model
    def _default_dest_address(self):
        res = self.get_parent_stock_data()
        if "dest_address_id" in res:
            return res["dest_address_id"]
        else:
            return super(ProjectProject, self)._default_dest_address()

    def compute_warehouse_id(self):
        for rec in self:
            if rec.location_id:
                rec.warehouse_id = rec.location_id.get_warehouse() or False
            else:
                rec.warehouse_id = False

    location_id = fields.Many2one(related="analytic_account_id.location_id")
    dest_address_id = fields.Many2one(
        related="analytic_account_id.dest_address_id"
    )
    will_buy = fields.Boolean()
    will_manufacture = fields.Boolean()
    picking_type_id = fields.Many2one("stock.picking.type")
    manufacture_picking_type_id = fields.Many2one("stock.picking.type")
    # todo find wh from location
    buy_rule_id = fields.Many2one("stock.rule")
    manufacture_rule_id = fields.Many2one("stock.rule")
    warehouse_id = fields.Many2one(
        "stock.warehouse", compute="compute_warehouse_id"
    )

    @api.multi
    def write(self, vals):
        if "will_buy" in vals:
            if vals.get("will_buy"):
                for pp in self:
                    if not pp.picking_type_id:
                        pp._create_project_buy_picking_type()
                    else:
                        pp.picking_type_id.active = True
                    # project rules:
                    pp._create_or_update_buy_pull()
            else:
                for pp in self:
                    pp.picking_type_id.active = False
        if "will_manufacture" in vals:
            if vals.get("will_manufacture"):
                for pp in self:
                    if not pp.manufacture_picking_type_id:
                        pp._create_project_manufacture_type()
                    else:
                        pp.manufacture_picking_type_id.active = True
                    # project rules:
                    pp._create_or_update_manufacture_pull()
                    pp.create_mrp_area()
            else:
                for pp in self:
                    pp.manufacture_picking_type_id.active = False
        return super(ProjectProject, self).write(vals)

    def _create_project_buy_picking_type(self):
        picking_type_obj = self.env["stock.picking.type"]
        customer_loc, supplier_loc = self.warehouse_id._get_partner_locations()
        wh = self.warehouse_id
        other_pick_type = picking_type_obj.search(
            [("warehouse_id", "=", wh.id)], order="sequence desc", limit=1
        )
        color = other_pick_type.color if other_pick_type else 0
        max_sequence = other_pick_type and other_pick_type.sequence or 0
        in_sequence = self.env["ir.sequence"].search(
            [("prefix", "=", "WH/IN/")], limit=1
        )
        # create project_cust_in_type_id:
        project_in_type_id = picking_type_obj.create(
            {
                "name": _("%s - Receipts" % self.name),
                "warehouse_id": wh.id,
                "code": "incoming",
                "use_create_lots": True,
                "use_existing_lots": False,
                "sequence_id": in_sequence.id,
                "default_location_src_id": supplier_loc.id,
                "default_location_dest_id": self.location_id.id,
                "sequence": max_sequence,
                "color": color,
            }
        )
        self.picking_type_id = project_in_type_id

    def _create_project_manufacture_type(self):
        picking_type_obj = self.env["stock.picking.type"]
        wh = self.warehouse_id
        other_pick_type = picking_type_obj.search(
            [("warehouse_id", "=", wh.id)], order="sequence desc", limit=1
        )
        color = other_pick_type.color if other_pick_type else 0
        max_sequence = other_pick_type and other_pick_type.sequence or 0
        in_sequence = self.env["ir.sequence"].search(
            [("prefix", "=", "WH/MO/")], limit=1
        )
        # create project_cust_in_type_id:
        manufacture_picking_type_id = picking_type_obj.create(
            {
                "name": _("%s - Manufacture" % self.name),
                "warehouse_id": wh.id,
                "code": "incoming",
                "use_create_lots": True,
                "use_existing_lots": False,
                "sequence_id": in_sequence.id,
                "default_location_src_id": self.location_id.id,
                "default_location_dest_id": self.location_id.id,
                "sequence": max_sequence,
                "color": color,
            }
        )
        self.manufacture_picking_type_id = manufacture_picking_type_id

    @api.multi
    def _create_or_update_buy_pull(self):
        self.ensure_one()
        rule_obj = self.env["stock.rule"]
        project_rules = dict()
        customer_loc, supplier_loc = self.warehouse_id._get_partner_locations()
        project_rules = {
            "name": _("Buy - %s" % self.name),
            "action": "buy",
            "warehouse_id": self.warehouse_id.id,
            "company_id": self.company_id.id,
            "location_src_id": supplier_loc.id,
            "location_id": self.location_id.id,
            "procure_method": "make_to_stock",
            "route_id": self.env.ref("purchase_stock.route_warehouse0_buy").id,
            "picking_type_id": self.picking_type_id.id,
            "active": True,
        }
        rule = rule_obj.create(project_rules)
        self.buy_rule_id = rule.id

    @api.multi
    def _create_or_update_manufacture_pull(self):
        self.ensure_one()
        rule_obj = self.env["stock.rule"]
        project_rules = dict()
        customer_loc, supplier_loc = self.warehouse_id._get_partner_locations()
        project_rules = {
            "name": _("Manufacture - %s" % self.name),
            "action": "manufacture",
            "warehouse_id": self.warehouse_id.id,
            "company_id": self.company_id.id,
            "location_src_id": supplier_loc.id,
            "location_id": self.location_id.id,
            "procure_method": "make_to_order",
            "route_id": self.env.ref("mrp.route_warehouse0_manufacture").id,
            "picking_type_id": self.manufacture_picking_type_id.id,
            "active": True,
        }
        rule = rule_obj.create(project_rules)
        self.manufacture_rule_id = rule.id

    def create_mrp_area(self):
        line = self
        mrp_area_obj = self.env["mrp.area"]
        area = mrp_area_obj.create(
            {
                "name": self.name,
                "location_id": self.location_id.id,
                "warehouse_id": self.warehouse_id.id,
            }
        )
        self.location_id.mrp_area_id = area.id
