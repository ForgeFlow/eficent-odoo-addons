# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm


class account_invoice_line(orm.Model):
    _inherit = "account.invoice.line"

    def move_line_get_item(self, cr, uid, line, context=None):
        uom_obj = self.pool.get('product.uom')
        currency_obj = self.pool.get('res.currency')
        res = super(account_invoice_line, self).move_line_get_item(
            cr, uid, line, context=context)
        moves_price = 0.0
        total_qty = 0.0
        if (
            line.invoice_id.type not in ('in_invoice', 'in_refund')
            or line.product_id.valuation != 'real_time'
        ):
            return res
        if line.move_line_ids:
            for move in line.move_line_ids:
                qty = uom_obj._compute_qty(cr, uid, move.product_uom.id,
                                           move.product_qty,
                                           move.product_id.uom_id.id)
                total_qty += qty
                if move.product_id.cost_method == 'average' \
                        and move.price_unit:
                    price_unit = currency_obj.compute(
                        cr, uid, line.invoice_id.currency_id.id,
                        move.price_currency_id.id, move.price_unit,
                        round=False)
                    moves_price += price_unit * qty
                else:
                    price_unit = currency_obj.compute(
                        cr, uid, line.invoice_id.currency_id.id,
                        move.price_currency_id.id,
                        move.product_id.standard_price, round=False)
                    moves_price += price_unit * qty
            res['price'] = moves_price
            res['price_unit'] = moves_price / total_qty
        return res

    def move_line_get(self, cr, uid, invoice_id, context=None):
        res = super(account_invoice_line, self).move_line_get(
            cr, uid, invoice_id, context=context)
        inv = self.pool.get('account.invoice').browse(
            cr, uid, invoice_id, context=context)

        if inv.type in ('in_invoice', 'in_refund'):
            for i_line in inv.invoice_line:
                if (
                    i_line.product_id
                    and i_line.product_id.valuation == 'real_time'
                    and i_line.product_id.type != 'service'
                    and i_line.move_line_ids
                ):
                    # get the price difference account at the product
                    acc = i_line.product_id.\
                        property_account_creditor_price_difference \
                        and i_line.product_id.\
                        property_account_creditor_price_difference.id
                    if not acc:
                        # if not found on the product get the price
                        # difference account at the category
                        acc = i_line.product_id.categ_id.\
                            property_account_creditor_price_difference_categ \
                            and i_line.product_id.categ_id.\
                            property_account_creditor_price_difference_categ.id
                    a = None

                    # oa will be the stock input account
                    # first check the product, if empty check the category
                    oa = i_line.product_id.property_stock_account_input \
                        and i_line.product_id.property_stock_account_input.id
                    if not oa:
                        oa = i_line.product_id.categ_id.\
                            property_stock_account_input_categ \
                            and i_line.product_id.categ_id.\
                            property_stock_account_input_categ.id

                    if oa:
                        # get the fiscal position
                        fpos = i_line.invoice_id.fiscal_position or False
                        a = self.pool.get('account.fiscal.position').\
                            map_account(cr, uid, fpos, oa)
                    diff_res = []
                    # calculate and write down the possible price difference
                    # between invoice price and product price
                    for line in res:
                        if a == line['account_id'] \
                                and i_line.product_id.id == line['product_id']:
                            if line['price'] != i_line.price_subtotal and acc:
                                price_diff = \
                                    i_line.price_subtotal - line['price']
                                diff_res.append({
                                    'type': 'src',
                                    'name': i_line.name[:64],
                                    'price_unit': price_diff,
                                    'quantity': line['quantity'],
                                    'price': price_diff,
                                    'account_id': acc,
                                    'product_id': line['product_id'],
                                    'uos_id': line['uos_id'],
                                    'account_analytic_id':
                                        line['account_analytic_id'],
                                    'taxes': line.get('taxes', []),
                                    })
                    res += diff_res
        return res
