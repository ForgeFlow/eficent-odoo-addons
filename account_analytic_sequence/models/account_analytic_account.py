# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Luxim d.o.o.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Deneroteam.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    @api.model
    def _create_sequence(self):
        ir_sequence_obj = self.env["ir.sequence"]
        account_sequence_obj = self.env["analytic.account.sequence"]
        ir_sequence_ids = ir_sequence_obj.search(
            [("code", "=", "account.analytic.account.code")]
        )
        vals = {}
        if ir_sequence_ids:
            ir_sequence = ir_sequence_ids[0]
            vals = {
                "analytic_account_id": self.id,
                "name": ir_sequence.name,
                "code": ir_sequence.code,
                "implementation": "no_gap",
                "active": ir_sequence.active,
                "prefix": ir_sequence.prefix,
                "suffix": ir_sequence.suffix,
                "number_next": 1,
                "number_increment": ir_sequence.number_increment,
                "padding": 2,
                "company_id": (
                    ir_sequence.company_id
                    and ir_sequence.company_id.id
                    or False
                ),
            }
        return account_sequence_obj.create(vals)

    sequence_ids = fields.One2many(
        "analytic.account.sequence",
        "analytic_account_id",
        string="Child code sequence",
    )
    code = fields.Char()

    @api.model
    def create(self, vals):
        # Assign a new code, from the parent account's sequence, if it exists.
        # If there's no parent, or the parent has no sequence, assign from
        # the basic sequence of the analytic account.
        account_obj = self.env["account.analytic.account"]
        obj_sequence = self.env["analytic.account.sequence"]
        if "parent_id" in vals and vals["parent_id"]:
            parent = account_obj.browse(vals["parent_id"])
            if parent.sequence_ids:
                new_code = obj_sequence.next_by_id(parent.sequence_ids[0].id)
            else:
                new_code = self.env["ir.sequence"].next_by_code(
                    "account.analytic.account.code"
                )
        else:
            new_code = self.env["ir.sequence"].next_by_code(
                "account.analytic.account.code"
            )
        if "code" not in vals and new_code:
            vals["code"] = new_code
        analytic_account = super(AccountAnalyticAccount, self).create(vals)
        if "sequence_ids" not in vals or (
            "sequence_ids" in vals and not vals["sequence_ids"]
        ) and not self._context.get('copy', False):
            analytic_account._create_sequence()
        return analytic_account

    @api.multi
    def write(self, vals):
        # If the parent project changes, obtain a new code according to the
        # new parent's sequence
        obj_sequence = self.env["analytic.account.sequence"]
        account_without_code = self.filtered(lambda a: not a.code)
        account_with_code = self - account_without_code
        res = True
        if account_with_code:
            res = res & super(
                AccountAnalyticAccount, account_with_code).write(vals)
        if "parent_id" in vals and vals["parent_id"] and 'code' not in vals:
            parent = self.browse(vals["parent_id"])
            if parent.sequence_ids:
                new_code = obj_sequence.next_by_id(parent.sequence_ids[0].id)
                vals.update({"code": new_code})
            if account_without_code:
                res = res & super(
                    AccountAnalyticAccount, account_without_code).write(
                    vals)
        return res

    @api.model
    def map_sequences(self, new_analytic_account):
        """ copy and map tasks from  old to new analytic account """
        account = self
        for sequence in account.sequence_ids:
            sequence.copy(
                {'analytic_account_id': new_analytic_account.id})
        return True

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        default["sequence_ids"] = []
        res = super(AccountAnalyticAccount,
                    self.with_context(copy=True)).copy(default)
        self.map_sequences(res)
        return res
