# -*- coding: utf-8 -*-
from odoo.api import Environment, SUPERUSER_ID
import logging
logger = logging.getLogger(__name__)


def post_init_hook(cr, pool):
    env = Environment(cr, SUPERUSER_ID, {})
    # avoid crashing installation because of having no active_analytic_planning_version
    active_analytic_planning_version = env.ref("analytic_plan.analytic_plan_version_P00")
    active_analytic_planning_version._write({'default_plan': True})
    for aa in env['account.analytic.account'].with_context(
            active_test=False).search([('active_analytic_planning_version', '=', False)]):
        aa._write({'active_analytic_planning_version': active_analytic_planning_version.id})
    logger.info('Assigning default plan version if not assigned')
