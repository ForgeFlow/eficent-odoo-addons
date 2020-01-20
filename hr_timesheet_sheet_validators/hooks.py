# Copyright 2014-20 ForgeFlow S.L.

from odoo.api import Environment, SUPERUSER_ID
import logging
logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    logger.info("Adding timesheet managers as validators in all timesheets")
    env = Environment(cr, SUPERUSER_ID, {})
    ts_mang_group_id = env.ref('hr_timesheet.group_timesheet_manager').id
    managers = env['res.users'].search(
        [('groups_id', '=', ts_mang_group_id)])
    timesheets = env['hr_timesheet.sheet'].search([])
    timesheets.write({'validator_user_ids': [(4, us.id) for us in managers]})
