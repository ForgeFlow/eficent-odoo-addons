from odoo import api, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.model
    def create(self, vals):
        emp = False
        if vals.get('product_id'):
            # do not override standard
            return super(AccountAnalyticLine, self).create(vals)
        elif vals.get('sheet_id'):
            sheet = self.env['hr_timesheet_sheet.sheet'].browse(
                vals.get('sheet_id'))
            emp = self.env['hr.employee'].search(
                [('id', '=', sheet.employee_id.id)], limit=1)
        if emp:
            vals.update(product_id=emp.product_id.id)
        return super(AccountAnalyticLine, self).create(vals)
