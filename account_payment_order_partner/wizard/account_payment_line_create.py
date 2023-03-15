# © 2009 EduSense BV (<http://www.edusense.nl>)
# © 2011-2013 Therp BV (<http://therp.nl>)
# © 2014-2015 ACSONE SA/NV (<http://acsone.eu>)
# © 2015-2016 Akretion (<http://www.akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountPaymentLineCreate(models.TransientModel):
    _inherit = "account.payment.line.create"

    partner_id = fields.Many2one("res.partner", string="Partner")

    @api.multi
    def _prepare_move_line_domain(self):
        res = super(AccountPaymentLineCreate, self)._prepare_move_line_domain()
        res.append(("partner_id", "=", self.partner_id.id))
        return res
