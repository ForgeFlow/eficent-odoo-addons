# 2015-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.multi
    def _account_entry_move(self, move):
        """
        If the location is a project location and it is out of the company do
        not create acc entries
        """
        if not move.analytic_account_id.location_id.company_id:
            return super(StockQuant, self)._account_entry_move(move)
        return False
