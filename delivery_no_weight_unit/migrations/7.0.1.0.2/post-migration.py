# Copyright 2011-17 Camptocamp SA
# Author: Nicolas Bessi.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):
    if not version:
        # only run at first install
        cr.execute("UPDATE stock_move " " SET weight_uom_id = NULL;")

        cr.execute("UPDATE stock_picking" " SET weight_uom_id = NULL;")
