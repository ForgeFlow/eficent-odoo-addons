from odoo.api import Environment, SUPERUSER_ID
import logging
logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    env = Environment(cr, SUPERUSER_ID, {})
    # creating missing anaytic journals if they are not created
    for aa in env['account.journal'].search(
            [('analytic_journal_id', '=', False)]):
        aa.analytic_journal_id = env['account.analytic.journal'].create(
            {'type': aa.type,
             'name': aa.name,
             'code': aa.code}
        )
