from odoo import fields, models


class Project(models.Model):
    _inherit = "project.project"

    cost_category = fields.Selection(
        [("cogs", "Cost of Goods Sold"), ("expense", "Expense")],
        string="Type of Cost",
        help="""Defines what type of cost does the analytic account carry
        from an employee perspective.""",
        default="cogs",
    )
