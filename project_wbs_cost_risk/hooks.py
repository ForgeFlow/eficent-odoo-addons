# Copyright 2021 ForgeFlow S.L.

from odoo import SUPERUSER_ID
from odoo.api import Environment


def post_init_hook(cr, pool):
    """
    By default control the cost in phases and deliverables
    """
    env = Environment(cr, SUPERUSER_ID, {})
    accounts = env["account.analytic.account"].search([])
    for account in accounts:
        if account.account_class in ("phase", "deliverable"):
            account.is_cost_controlled = True
        else:
            account.is_cost_controlled = False
