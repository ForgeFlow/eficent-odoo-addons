# -*- coding: utf-8 -*-
# © 2016 Odoo Community Association (https://odoo-community.org)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, models, fields, _


class LedgerReportWizard(models.TransientModel):
    _name = 'ledger.report.wizard'

    date = fields.Date('Date')

    def _query(self):
        query = """
              WITH view_q as (SELECT
                ml.date,
                acc.id AS account_id,
                ml.debit,
                ml.credit,
                SUM(debit) OVER w_account - debit AS init_debit,
                SUM(credit) OVER w_account - credit AS init_credit,
                SUM(debit - credit) OVER w_account - (debit - credit) AS init_balance,
                SUM(debit - credit) OVER w_account AS cumul_balance
              FROM
                account_account AS acc
                LEFT JOIN account_move_line AS ml ON (ml.account_id = acc.id)
                --INNER JOIN res_partner AS part ON (ml.partner_id = part.id)
              INNER JOIN account_move AS m ON (ml.move_id = m.id)
              WINDOW w_account AS (PARTITION BY acc.code ORDER BY ml.date, ml.id)
              ORDER BY acc.id, ml.date)
              SELECT * from view_q where date >= %s
            """

        params = (self.date,)
        self.env.cr.execute(query, params)

        return self.env.cr.fetchall()

    @api.multi
    def process(self):
            ledger_line_obj = self.env['ledger.report.wizard.line']
            rows = self._query()
            res = []
            for row in rows:
                data = {
                    'wiz_id': self.id,
                    'date': row[0],
                    'account_id': row[1],
                    'debit': row[2],
                    'credit': row[3],
                    'init_debit': row[4],
                    'init_credit': row[5],
                    'init_balance': row[6],
                    'cum_balance': row[7]
                }
                gll = ledger_line_obj.create(data)
                res.append(gll.id)

            return {
                'domain': "[('wiz_id','=', "+str(self.id)+")]",
                'name': _('Ledger lines'),
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'ledger.report.wizard.line',
                'view_id': False,
                'context': False,
                'type': 'ir.actions.act_window'
            }


class LedgerReportWizardLine(models.TransientModel):
    _name = 'ledger.report.wizard.line'

    wiz_id = fields.Many2one('ledger.report.wizard', required=True,
                             ondelete='cascade')
    date = fields.Date('Date')
    account_id = fields.Many2one('account.account', 'Account')
    debit = fields.Float('Debit')
    credit = fields.Float('Credit')
    init_debit = fields.Float('Initial debit')
    init_credit = fields.Float('Initial credit')
    init_balance = fields.Float('Initial balance')
    cum_balance = fields.Float('Cumulated Balance')
