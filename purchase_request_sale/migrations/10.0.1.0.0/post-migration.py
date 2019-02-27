# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from openupgradelib import openupgrade


def fill_purchase_request_sale_rel(env):
    env.cr.execute(
        """
            INSERT INTO purchase_request_sale_rel (request_id, sale_id)
            SELECT DISTINCT ON (so.id, pr.id) so.id as sale_id,
            pr.id as request_id
            FROM purchase_request pr
            INNER JOIN purchase_request_line prl on prl.request_id = pr.id
            INNER JOIN sale_order_line sol ON sol.id = prl.sale_order_line_id
            INNER JOIN sale_order so ON sol.order_id = so.id
        """
    )


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    fill_purchase_request_sale_rel(env)
