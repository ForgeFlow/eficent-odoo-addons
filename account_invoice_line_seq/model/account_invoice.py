# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import osv, fields


class AccountInvoiceLine(osv.osv):
    _inherit = 'account.invoice.line'

    _columns = {
        'sequence2': fields.related(
            'sequence',
            type='integer',
            relation='account.invoice.line',
            string='Sequence',
            help='Field to show the number of sequence in line')
    }
