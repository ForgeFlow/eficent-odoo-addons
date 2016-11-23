# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models, _


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    def _get_quants(self, cr, uid, line, context=None):
        quant_obj = self.pool["stock.quant"]
        dom = [('company_id', '=', line.company_id.id), ('location_id', '=', line.location_id.id), ('lot_id', '=', line.prod_lot_id.id),
                        ('product_id','=', line.product_id.id), ('owner_id', '=', line.partner_id.id), ('package_id', '=', line.package_id.id),
                        ('analytic_account_id', '=', line.analytic_account_id.id)]
        quants = quant_obj.search(cr, uid, dom, context=context)
        return quants


    @api.onchange('product_id', 'location_id', 'product_uom_id',
                  'analytic_account_id', 'location_id', 'package_id',
                  'partner_id')
    def onchange_line(self):
        quant_obj = self.env["stock.quant"]
        uom_obj = self.env["product.uom"]
        res = {'value': {}}
        # If no UoM already put the default UoM of the product
        if self.product_id:
            product = self.product_id
            uom = self.product_uom_id
            if product.uom_id.category_id.id != uom.category_id.id:
                self.product_uom_id = product.uom_id.id
                res['domain'] = {
                    'product_uom_id': [('category_id', '=',
                                        product.uom_id.category_id.id)]}
        # Calculate theoretical quantity by searching the quants as in
        # quants_get
        if self.product_id and self.location_id:
            product = self.product_id
            company_id = self.env['res.users'].browse(self._uid).\
                company_id.id
            dom = [('company_id', '=', company_id),
                   ('location_id', '=', self.location_id.id),
                   ('lot_id', '=', self.prod_lot_id.id),
                   ('product_id', '=', self.product_id.id),
                   ('owner_id', '=', self.partner_id.id),
                   ('package_id', '=', self.package_id.id),
                   ('analytic_account_id', '=', self.analytic_account_id.id)]
            quants = quant_obj.search(dom)
            th_qty = sum([x.qty for x in quants])
            if self.product_id and self.product_uom_id and\
                product.uom_id.id != self.product_uom_id:
                    th_qty = uom_obj._compute_qty(product.uom_id.id, th_qty,
                                              self.product_uom_id.id)
            self.theoretical_qty = th_qty
            self.product_qty = th_qty


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    analytic_account_id = fields.Many2one(
            'account.analytic.account', 'Analytic account')

    @api.multi
    def onchange_filter(self, filter):
        to_clean = super(StockInventory, self).onchange_filter(filter)
        for record in self:
            if filter != 'analytic':
                to_clean['value']['analytic_account_id'] = False
            return to_clean

    @api.model
    def _get_available_filters(self):
        """This function will return the list of filters allowed according to
        the options checked in 'Settings/Warehouse'.

        :return: list of tuple
        """
        res_filters = super(StockInventory, self)._get_available_filters()
        res_filters.append(('analytic', _('One Analytic Account')))
        return res_filters

    filter = fields.Selection(
        selection=_get_available_filters, string='Selection Filter',
        required=True)
