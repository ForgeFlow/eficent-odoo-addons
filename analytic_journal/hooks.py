from odoo.api import Environment, SUPERUSER_ID
import logging

logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    # avoid crashing installation because missing analytic journals
    logger.info("Creating analytic journals for all journals")
    for aj in env["account.journal"].search(
        [("analytic_journal_id", "=", False)]
    ):
        aaj = env["account.analytic.journal"].create(
            {"name": aj.name, "code": aj.code, "type": aj.type}
        )
        aj.analytic_journal_id = aaj.id
