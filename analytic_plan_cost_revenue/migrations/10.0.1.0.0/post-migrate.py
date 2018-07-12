# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import odoo


def force_recompute_contract_value(env):
    lines = env['account.analytic.account'].search([])
    lines.get_analytic_totals()
    lines.get_analytic_plan_totals()


def migrate(cr, version):
    if not version:
        # installation of the module
        return
    with odoo.api.Environment.manage():
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        force_recompute_contract_value(env)
