from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    def action_done(self):
        res = super(StockMove, self).action_done()
        self.create_analytic_resource_plan_line()
        return res

    def _check_new_resource_is_needed(self):
        """
        From a stock move returns:
        1. if a new resource should be created
        2. if an exising resoruce should be update
        3. an existing resource, not linked to any purchase request

        """
        self.ensure_one()
        if not self.analytic_account_id:
            return False, False, False
        else:
            # we check if the stock moves comes from a po line, if so, we check if
            # there are resources associated
            if self.purchase_line_id.purchase_request_lines.mapped(
                "analytic_resource_plan_lines"
            ):
                # id the resource was the origin of the pull request we have to do
                # nothing
                return False, False, False
            else:
                # we have to check if we have to update a resource or just create a
                # new one
                existing_resource = self.env[
                    "analytic.resource.plan.line"
                ].search(
                    [
                        ("account_id", "=", self.analytic_account_id.id),
                        ("product_id", "=", self.product_id.id),
                        ("purchase_request_lines", "=", False),
                    ]
                )
                if existing_resource:
                    return False, True, existing_resource
                else:
                    return True, False, False

    def _prepare_anlaytic_resource_plan_vals(self):
        self.ensure_one()
        if self.product_id.uom_id.name == "Hour(s)":
            resource_type = "task"
        else:
            resource_type = "procurement"
        res = {
            "account_id": self.analytic_account_id.id,
            "name": self.product_id.name,
            "date": self.date,
            "state": "confirm",
            "product_id": self.product_id.id,
            "product_uom_id": self.product_id.uom_id.id,
            "unit_amount": self.product_uom_qty,
            "price_unit": self.price_unit,
            "bom_id": False,
            "parent_id": False,
            "resource_type": resource_type,
        }
        return res

    def _prepare_update_analytic_resource_plan_vals(self, existing_resource):
        "Just add the qty in the stock move to an existing resource"
        self.ensure_one()
        try:
            # get the average
            new_price_unit = (
                (existing_resource.price_unit * existing_resource.unit_amount)
                + (self.product_uom_qty * self.price_unit)
            ) / (self.product_uom_qty + existing_resource.unit_amount)
        except ZeroDivisionError:
            new_price_unit = existing_resource.price_unit
        res = {
            "unit_amount": existing_resource.unit_amount + self.product_uom_qty,
            "price_unit": new_price_unit,
        }
        return res

    def create_analytic_resource_plan_line(self):
        for move in self:
            (
                should_create,
                should_update,
                existing_resource,
            ) = move._check_new_resource_is_needed()
            if should_create:
                resource_plan_vals = move._prepare_anlaytic_resource_plan_vals()
                self.env["analytic.resource.plan.line"].create(
                    resource_plan_vals
                )
            elif should_update and existing_resource:
                resource_plan_vals = (
                    move._prepare_update_analytic_resource_plan_vals(
                        existing_resource
                    )
                )
                existing_resource.update(resource_plan_vals)
