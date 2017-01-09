from openerp.osv import fields, osv, orm
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp import tools

class StockChangeProductQty(osv.osv_memory):
    _inherit = "stock.change.product.qty"

    def _check_location_analytic(self, cr, uid, ids, field_names, arg,
                                 context=None):
        res = {}
        for wiz in self.browse(cr, uid, ids):
            if wiz.location_id.analytic_account_id:
                res[wiz.id] = {
                        'analytic_account_id':
                            wiz.location_id.analytic_account_id.id,
                    }
            else:
                res[wiz.id] = {
                    'analytic_account_id': False,
                }
        return res

    _columns = {
        'analytic_account_id': fields.function(
            _check_location_analytic,
            type='many2one',
            relation="account.analytic.account",
            string="Analytic Account",
            multi="analytic"),
    }
