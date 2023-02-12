# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from datetime import datetime


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    budget_hours = fields.Float(
        default=0,
        string="Budget Hours",
        help="Set manually the estimated hours for the project",
    )
    actual_hours = fields.Float(compute="_compute_actual_project_hours", store=True)
    budget_hours_percentage = fields.Float(compute="_compute_budget_hours_percentage", store=True, string="Cost Alert")
    cost_alert_color = fields.Integer(compute="_compute_cost_alert_color", store=True)
    is_cost_controlled = fields.Boolean()

    @api.multi
    def _compute_cost_alert_color(self):
        "The recomputation will be triggered by the cron not the api.depends"
        for account in self:
            if account.budget_hours_percentage < 50:
                if account.is_cost_controlled and account.cost_alert_color != 0:
                    account.cost_risk_notify(account.cost_alert_color, 0)
                account.cost_alert_color = 0
            elif account.budget_hours_percentage >= 50 and account.budget_hours_percentage < 70:
                if account.is_cost_controlled and account.cost_alert_color != 1:
                    account.cost_risk_notify(account.cost_alert_color, 1)
                account.cost_alert_color = 1
            elif account.budget_hours_percentage >= 70 and account.budget_hours_percentage <= 85:
                if account.is_cost_controlled and account.cost_alert_color != 2:
                    account.cost_risk_notify(account.cost_alert_color, 2)
                account.cost_alert_color = 2
            elif account.budget_hours_percentage >= 85 and account.budget_hours_percentage <= 100:
                if account.is_cost_controlled and account.cost_alert_color != 3:
                    account.cost_risk_notify(account.cost_alert_color, 3)
                account.cost_alert_color = 3
            else:
                if account.is_cost_controlled and account.cost_alert_color != 4:
                    account.cost_risk_notify(account.cost_alert_color, 4)
                account.cost_alert_color = 4

    @api.multi
    @api.depends("budget_hours", "is_cost_controlled")
    def _compute_budget_hours_percentage(self):
        "The recomputation will be triggered by the cron not the api.depends"
        for account in self:
            if account.budget_hours == 0:
                budget_hours_percentage = 0
            elif not account.is_cost_controlled:
                budget_hours_percentage = 0
            else:
                budget_hours_percentage = (account.actual_hours / account.budget_hours)*100
            account.budget_hours_percentage = budget_hours_percentage

    @api.multi
    @api.depends("budget_hours", "is_cost_controlled")
    def _compute_actual_project_hours(self):
        "The recomputation will be triggered by the cron not the api.depends"
        # Do not count future hours
        to_date = datetime.strftime(datetime.today(), DF)
        where_date = " AND l.date <= %s"
        # compute sql based because the child_of domain does not work
        # so cannot use read_group
        for account in self:
            all_ids = account.get_child_accounts().keys()
            if not len(all_ids):
                continue
            # Actual costs
            query_params = [tuple(all_ids)]
            query_params += [to_date]
            cr = self._cr
            cr.execute(
                """
                SELECT unit_amount
                FROM account_analytic_line AS L
                LEFT JOIN account_analytic_account AS A
                ON L.account_id = A.id
                INNER JOIN account_analytic_journal AS AAJ
                ON AAJ.id = L.journal_id
                AND AAJ.cost_type = 'labor'
                INNER JOIN account_account AC
                ON L.general_account_id = AC.id
                INNER JOIN account_account_type AT
                ON AT.id = AC.user_type_id
                WHERE AT.name in ('Expense', 'Cost of Goods Sold',
                'Expenses', 'Cost of Revenue')
                AND L.account_id IN %s
                """ + where_date + """
                """,
                query_params
            )
            all_data = cr.fetchall()
            if all_data:
                actual_hours = sum([r[0] or 0 for r in all_data])
            else:
                actual_hours = 0
            account.actual_hours = actual_hours

    @api.multi
    def cost_risk_notify(self, previous_cost_risk, new_cost_risk):
        self.ensure_one()
        project_manager_id = self.user_id and \
        self.user_id.partner_id.id or False
        # add the project manager as follower
        if project_manager_id:
            message_follower_ids = [x.partner_id.id for x in
                                    self.message_follower_ids]

            if project_manager_id not in message_follower_ids:
                reg = {
                    'res_id': self.id,
                    'res_model': 'account.analytic.account',
                    'partner_id': project_manager_id,
                }
                self.env['mail.followers'].sudo().create(reg)
        # add followers of the project to follow the analytic account
        for follower in self.project_ids.mapped('message_follower_ids.partner_id'):
            message_follower_ids = [x.partner_id.id for x in
                        self.message_follower_ids]
            if follower.id not in message_follower_ids:
                reg = {
                    'res_id': self.id,
                    'res_model': 'account.analytic.account',
                    'partner_id': follower.id,
                }
                self.env['mail.followers'].sudo().create(reg)
        # notify risk change
        message = self._risk_change_message_content(previous_cost_risk, new_cost_risk)
        self.message_post(body=message, subtype='mail.mt_comment', partner_ids=message_follower_ids)

    @api.multi
    def _risk_change_message_content(self, previous_cost_risk, new_cost_risk):
        self.ensure_one()
        title = _('Project Cost Risk Update for account %s') % (
            self.complete_wbs_code)
        message = '<h3>%s</h3><ul>' % title
        risk_status_text = self.get_risk_text(new_cost_risk)
        previous_risk_status_text = self.get_risk_text(previous_cost_risk)
        message += _('The project passed from %s '
                     'to %s') % (
            previous_risk_status_text, risk_status_text)
        return message

    @api.model
    def get_risk_text(self, risk):
        if risk == 1:
            return "Low Cost Risk"
        elif risk == 2:
            return "Medium Cost Risk"
        elif risk == 3:
            return "High Cost Risk"
        elif risk == 4:
            return "Cost Exceeded"
        else:
            return "No risk"

    @api.model
    def _get_analytic_cost_risk_domain(self):
        return [('stage_id', 'not ilike', 'Closed')]

    @api.model
    def cron_calculate_cost_risk(self):
        domain = self._get_analytic_cost_risk_domain()
        accounts = self.search(domain)
        accounts._compute_actual_project_hours()
        accounts._compute_budget_hours_percentage()
        accounts._compute_cost_alert_color()
