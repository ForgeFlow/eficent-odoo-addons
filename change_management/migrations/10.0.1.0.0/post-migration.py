# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from openupgradelib import openupgrade


def assign_user_and_dates(env):
    env.cr.execute("""
        select id, change_owner_id, date_modified
        from change_management_change
    """)
    for (ch_id, change_owner_id, date_modified) in env.cr.fetchall():
        ch = env['change.management.change'].browse(ch_id)
        ch.write({'date_confirmed': date_modified,
                  'date_approved': date_modified,
                  'approved_id': change_owner_id,
                  'confirmed_id': change_owner_id
                  })


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    assign_user_and_dates(env)
