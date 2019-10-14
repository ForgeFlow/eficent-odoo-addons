# Copyright 2014-17 Eficent Business and IT Consulting Services S.L.
# Copyright 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class Product(models.Model):

    _inherit = "product.product"

    def _get_domain_locations(self):

        if self._context.get('analytic_account_id'):
            aa = self.env['account.analytic.account'].browse(
                self._context.get('analytic_account_id'))
            return super(Product, self.with_context(
                location=aa.location_id.id))._get_domain_locations()
        else:
            return super(Product, self)._get_domain_locations()
