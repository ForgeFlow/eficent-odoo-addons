from odoo import api, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.model
    def create(self, vals):
        emp = False
        if vals.get("product_id"):
            # do not override standard
            return super(AccountAnalyticLine, self).create(vals)
        elif vals.get("sheet_id"):
            sheet = self.env["hr_timesheet.sheet"].browse(vals.get("sheet_id"))
            emp = self.env["hr.employee"].search(
                [("id", "=", sheet.employee_id.id)], limit=1
            )
        if emp:
            if vals.get("unit_amount"):
                vals.update(
                    amount=emp.product_id.standard_price
                    * vals.get("unit_amount")
                )
            vals.update(product_id=emp.product_id.id)
        return super(AccountAnalyticLine, self).create(vals)

    @api.multi
    def write(self, vals):
        for a in self:
            if a.sheet_id and vals.get("unit_amount"):
                if a.product_id.is_employee:
                    amount = a.product_id.standard_price * vals.get(
                        "unit_amount"
                    )
                if amount:
                    vals.update(amount=amount)
        return super(AccountAnalyticLine, self).write(vals)
