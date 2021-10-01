# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


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
            elif account.budget_hours_percentage >= 50 and account.budget_hours_percentage < 67:
                if account.is_cost_controlled and account.cost_alert_color != 1:
                    account.cost_risk_notify(account.cost_alert_color, 1)
                account.cost_alert_color = 1
            elif account.budget_hours_percentage >= 67 and account.budget_hours_percentage <= 83:
                if account.is_cost_controlled and account.cost_alert_color != 2:
                    account.cost_risk_notify(account.cost_alert_color, 2)
                account.cost_alert_color = 2
            elif account.budget_hours_percentage >= 84 and account.budget_hours_percentage <= 100:
                if account.is_cost_controlled and account.cost_alert_color != 3:
                    account.cost_risk_notify(account.cost_alert_color, 3)
                account.cost_alert_color = 3
            else:
                if account.is_cost_controlled and account.cost_alert_color != 4:
                    account.cost_risk_notify(account.cost_alert_color, 4)
                account.cost_alert_color = 4

    @api.multi
    @api.depends("budget_hours")
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
    @api.depends("budget_hours")
    def _compute_actual_project_hours(self):
        "The recomputation will be triggered by the cron not the api.depends"
        analytic_line_obj = self.env["account.analytic.line"]
        # compute only sheet analytic lines
        for account in self:
            domain = [
                ("account_id", "child_of", account.ids),
                ("sheet_id", "!=", False),
            ]
            anal_groups = analytic_line_obj.read_group(
                domain, fields=["account_id", "unit_amount"], groupby=["account_id"],
            )
            actual_hours = sum(l["unit_amount"] for l in anal_groups)
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
        self.message_post(body=message, subtype='mail.mt_comment')

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
