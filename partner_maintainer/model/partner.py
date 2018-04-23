# -*- coding: utf-8 -*-
# Copyright Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm
from openerp.tools.translate import _
from openerp import exceptions


class ResPartner(orm.Model):
    _inherit = "res.partner"

    def write(self, cr, uid, ids, vals, context=None):
        if any([k in vals for k in ['street', 'street2','zip_id', 'street3', 'city', 'state_id', 'zip', 'country_id']]):
            for partner_id in ids:
                partner = self.browse(cr, uid, partner_id)
                moves = self.pool.get('account.move').search(cr, uid, [('partner_id', '=', partner_id)])
                invoices = self.pool.get('account.invoice').search(
                    cr, uid, [('partner_id', '=', partner.commercial_partner_id.id),
                              ('state', '!=', 'cancel')])
                if moves or invoices:
                    if not self.pool['res.users'].has_group(cr, uid, 'partner_maintainer.group_partner_maintainer'):
                        raise exceptions.AccessError(
                            _("Only administrators can change partner addresses"))

        return super(ResPartner, self).write(
            cr, uid, ids, vals, context)
