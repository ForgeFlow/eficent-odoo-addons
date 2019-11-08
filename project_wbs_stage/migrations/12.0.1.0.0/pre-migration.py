# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def fill_stages(cr):

    cr.execute("SELECT id FROM ir_model WHERE "
               "model = 'account.analytic.account'")
    analytic_model_id = cr.fetchone()
    query = """
        INSERT INTO base_kanban_stage (
            id,
            name,
            description,
            fold,
            sequence,
            create_date,
            write_date,
            create_uid,
            write_uid,
            res_model_id
        )
        SELECT
            aas.id,
            aas.name,
            aas.description,
            aas.fold,
            aas.sequence,
            aas.create_date,
            aas.write_date,
            aas.create_uid,
            aas.write_uid,
            %s
        FROM analytic_account_stage AS aas
        ON CONFLICT DO NOTHING
    """ % analytic_model_id
    openupgrade.logged_query(cr, query)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    # base_kanban_stage already installed
    if openupgrade.table_exists(cr, 'analytic_account_stage'):
        fill_stages(cr)
