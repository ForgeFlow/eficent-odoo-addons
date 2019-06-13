# -*- coding: utf-8 -*-

from odoo import api, models


class AccountAnalyticAccount(models.Model):

    _inherit ='account.analytic.account'

    @api.multi
    def get_parents(self):
        """
        get all parents given a child analytic account
        """
        res = []
        for account in self:
            current = account
            res.append(current.id)
            while current.parent_id:
                res.append(current.parent_id.id)
                current = current.parent_id
        print(res)
        return res
