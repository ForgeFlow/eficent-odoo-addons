# Copyright 2017 ForgeFlow S.L.
#   (http://www.ForgeFlow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AnalyticMilestoneInvoicing(models.TransientModel):
    _name = "analytic.milestone.invoice"
    _description = "Analytic Milestone Invoicing"

    item_ids = fields.One2many(
        comodel_name='analytic.milestone.invoice.item',
        inverse_name='wiz_id',
        string="Milestones to invoice")
    partner_id = fields.Many2one('res.partner', "Partner in the invoice")

    def _prepare_item(self, mil):
        milestone = self.env['analytic.milestone'].browse(mil)
        account = (milestone.account_id.milestone_product_id.
                   property_account_income_id or
                   milestone.account_id.milestone_product_id.categ_id.
                   property_account_income_categ_id)
        values = {'milestone_id': mil,
                  'name': milestone.name,
                  'account_id': account.id or False
                  }
        return values

    @api.model
    def default_get(self, fields):
        res = super(AnalyticMilestoneInvoicing, self).default_get(fields)
        milestone_ids = self._context.get('active_ids', [])
        active_model = self._context.get('active_model')
        if not milestone_ids:
            return res
        assert active_model == 'analytic.milestone', \
            'Bad context propagation'
        items = []
        for mil in milestone_ids:
            items.append((0, 0, self._prepare_item(mil)))
        res['item_ids'] = items
        # check bounds
        milestones = self.env['analytic.milestone'].browse(milestone_ids)
        milestones.check_bounds()
        partner_id = self.env['analytic.milestone'].browse(
            milestone_ids).mapped('account_id.partner_id')[0]

        res['partner_id'] = partner_id.id
        return res

    @api.multi
    def action_invoice_create(self):
        invoice_obj = self.env['account.invoice']
        invoices = {}
        references = {}
        invoices_origin = {}
        invoices_name = {}
        for plan in self.item_ids:
            mil = plan.milestone_id
            group_key = (self.partner_id.id, mil.milestone_date)
            if group_key not in invoices:
                inv_data = mil._prepare_invoice(self.partner_id)
                invoice = invoice_obj.create(inv_data)
                references[invoice] = mil
                invoices[group_key] = invoice
                invoices_origin[group_key] = [invoice.origin]
                invoices_name[group_key] = [invoice.name]
            elif group_key in invoices:
                if mil.display_name not in invoices_origin[group_key]:
                    invoices_origin[group_key].append(mil.display_name)
                if mil.display_name not in invoices_name[group_key]:
                    invoices_name[group_key].append(mil.display_name)
            mil.invoice_line_create(
                invoices[group_key].id, mil.percent / 100.0,
                plan.wiz_id.partner_id,
                plan.account_id)
            mil.invoice_id = invoices[group_key]
            if references.get(invoices.get(group_key)):
                if mil not in references[invoices[group_key]]:
                    references[invoices[group_key]] |= mil
        for group_key in invoices:
            invoices[group_key].write({
                'name': ', '.join(invoices_name[group_key]),
                'origin': ', '.join(invoices_origin[group_key]),
            })
        if not invoices:
            raise ValidationError(_('There is no invoiceable milestone.'))
        for invoice in invoices.values():
            invoice.compute_taxes()


class AnalyticMilestoneInvoicingItem(models.TransientModel):
    _name = "analytic.milestone.invoice.item"
    _description = "Analytic Milestone Invoicing Item"

    name = fields.Char(
        'Description',
        related='milestone_id.name'
    )
    wiz_id = fields.Many2one(
        'analytic.milestone.invoice',
        string='Wizard', required=True, ondelete='cascade',
        readonly=True)
    milestone_id = fields.Many2one('analytic.milestone',
                                   string='Milestone',
                                   required=True,
                                   ondelete='cascade')
    account_id = fields.Many2one(
        'account.account',
        string='Income Account', readonly=False)
