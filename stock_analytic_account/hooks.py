# Copyright 2014-17 Eficent Business and IT Consulting Services S.L.
# Copyright 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.api import Environment, SUPERUSER_ID
import logging
logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    env = Environment(cr, SUPERUSER_ID, {})
    # creating missing anaytic journals if they are not created
    for aa in env['account.journal'].with_context(active_test=False).search(
            [('analytic_journal_id', '=', False)]):
        aa.analytic_journal_id = env['account.analytic.journal'].create(
            {'type': aa.type,
             'name': aa.name,
             'code': aa.code}
        )
