# Copyright 2015 Odoo SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lpgl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    journal_id = fields.Many2one("account.analytic.journal", "Analytic Journal")


class AccountAnalyticJournal(models.Model):
    _name = "account.analytic.journal"
    _description = "Analytic Journal"

    name = fields.Char(string="Journal Name", required=True)
    code = fields.Char(string="Short Code", size=5, required=True)
    type = fields.Selection(
        [
            ("sale", "Sale"),
            ("purchase", "Purchase"),
            ("cash", "Cash"),
            ("bank", "Bank"),
            ("general", "Miscellaneous"),
        ],
        required=True,
        help="Select 'Sale' for customer invoices journals. Select 'Purchase'"
        " for vendor bills journals. Select 'Cash' or 'Bank' for "
        "journals that are used in customer or vendor payments."
        "Select 'General' for miscellaneous operations journals.",
    )

    line_ids = fields.One2many(
        "account.analytic.line", "journal_id", "Lines", copy=False
    )
    company_id = fields.Many2one(
        comodel_name="res.company", default=lambda self: self._get_default_company()
    )

    @api.model
    def find_journal(self, vals=None):
        if vals and vals.get("code", False):
            self.search([("code", "=", vals["code"])])
        return None

    @api.model
    def _prepare_analytic_journal(self, vals):
        if vals.get("type") and vals.get("name") and vals.get("code"):
            vals = {"type": vals["type"], "name": _(vals["name"]), "code": vals["code"]}
        else:
            raise ValidationError(_("Cannot create an analytic journal"))
        return vals

    def _get_default_company(self):
        return self.env.user.company_id.id


class AccountJournal(models.Model):
    _inherit = "account.journal"

    analytic_journal_id = fields.Many2one(
        "account.analytic.journal",
        "Analytic Journal",
        help="Journal for analytic entries",
    )


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _prepare_analytic_line(self):
        res = super(AccountMoveLine, self)._prepare_analytic_line()
        for move_line in self:
            if not move_line.journal_id.analytic_journal_id:
                raise ValidationError(
                    _(
                        "Please define an analytic journal for "
                        "journal %s" % move_line.journal_id.name
                    )
                )
            for line in res:
                if line.get("move_id") == move_line.id:
                    line["journal_id"] = move_line.journal_id.analytic_journal_id.id
                    break
        return res
