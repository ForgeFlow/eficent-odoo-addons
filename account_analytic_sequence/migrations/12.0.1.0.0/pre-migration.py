# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade

xmlid_renames = [
    ('account_analytic_sequence.seq_analytic_account_sequence_default',
     'account_analytic_sequence.analytic_account_code_seq'),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(env.cr, xmlid_renames)
