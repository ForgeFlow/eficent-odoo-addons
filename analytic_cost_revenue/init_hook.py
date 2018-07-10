# -*- coding: utf-8 -*-
# © 2016 David Dufresne <david.dufresne@savoirfairelinux.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging


logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    """
    The objective of this hook is to speed up the installation
    of the module on an existing Odoo instance.

    Without this script, if a database has a few hundred thousand
    journal entries, which is not unlikely, the update will take
    at least a few hours.

    The pre init script only writes 0 in the field maturity_residual
    so that it is not computed by the install.

    The post init script sets the value of maturity_residual.
    """
    store_field_stored_invoice_id(cr)


def store_field_stored_invoice_id(cr):
    cr.execute(
        """
        UPDATE account_analytic_account aa
        SET (labor_cost, material_cost, total_cost, revenue, gross_profit) =
         (0.0, 0.0, 0.0, 0.0, 0.0)
        """
    )
