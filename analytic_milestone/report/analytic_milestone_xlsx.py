# Copyright 2017 ForgeFlow S.L.
#   (http://www.ForgeFlow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DT


class AnalyticMilestoneReport(models.TransientModel):
    _name = 'report.analytic_milestone.analytic_milestone_xlsx'
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, objects):
        if not data.get('wizard'):
            milestones = objects
        else:
            milestones = self.env['analytic.milestone'].browse(data['data'])
        if not data.get('report_type'):
            report_type = 'milestone'
        else:
            report_type = data['report_type']
        if not data.get('invoice_id'):
            invoice_id = False
        else:
            invoice_id = data['invoice_id']
        milestones.check_bounds()
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 10.0'})
        sheet = workbook.add_worksheet(_('Invoicing Process'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(80)
        sheet.set_column(0, 0, 20)
        sheet.set_column(1, 1, 10)
        sheet.set_column(2, 2, 40)
        sheet.set_column(3, 10, 20)

        bold = workbook.add_format({'bold': True})
        title_style = workbook.add_format({'bold': True,
                                           'bg_color': '#FFFFCC',
                                           'bottom': 1})
        total_style = workbook.add_format({'bold': True,
                                           'bg_color': '#00FFFF',
                                           'top': 1})
        subtotal_style = workbook.add_format({'bold': True,
                                              'bg_color': '#F5F5F5',
                                              'top': 1,
                                              'bottom': 1,
                                              'right': 1,
                                              'left': 1})
        sheet_title = [_('Item No.'),
                       _('Milestone\nPercent'),
                       _('Description'),
                       _('Base Contract\nAmount'),
                       _('Retention 10%'),
                       _('Approval Date'),
                       _('Milestone Date'),
                       _('Billing Date'),
                       _('Invoice Amount'),
                       _('Previous Payments'),
                       _('This invoice'),
                       ]
        sheet_summary = ["Invoicing Process to submit documents required "
                         " for ASTS payment milestiones by 30th of each month"
                         " (Month X)\nASTS to include documents in invoice"
                         " request by 3TC by 15th of following month"
                         " (Month X+1) \n3TC to confirm invoice approval"
                         " usually afer 5 days from ASTS invoice request\n"
                         "ASTS to authorize the company to Invoice 5 days "
                         " after receiving 3TC confirmation of invoicing "
                         "approval.\nAll milestones are back to back "]
        sheet.set_row(0, None, None, {'collapsed': 1})
        sheet.set_row(1, 80)
        sheet.write_row(1, 0, sheet_summary)

        sheet.write_row(3, 0, milestones.mapped('account_id.name'))
        sheet.write_row(3, 3, milestones.mapped(
            'invoice_line_ids.invoice_id.name') or milestones.mapped(
            'account_id.partner_id.name'))

        sheet.write_row(4, 3, ["Requested Milestone Payment No X"])
        sheet.write_row(5, 3, ["Invoice No X"])
        sheet.write_row(6, 0, "")

        sheet.set_row(7, 40)
        sheet.write_row(7, 0, sheet_title, title_style)
        sheet.freeze_panes(2, 0)
        total_base_amount = 0
        total_retention = 0
        total_previous_amount = 0
        total_next_amount = 0
        total_invoice_amount = 0
        total_amount_residual = 0
        i = 9
        invoice_residual_included = []
        date = self.env['account.invoice'].browse(invoice_id).date_invoice
        if report_type == 'invoice':
            for o in milestones:
                all_invl = o.invoice_line_ids
                prev_invl = o.invoice_line_ids.filtered(
                    lambda il: il.invoice_id.date_invoice <= date)
                this_invl = o.invoice_line_ids.filtered(
                    lambda il: il.invoice_id.id == invoice_id)

                prev_amount = sum(prev_invl.mapped('price_subtotal'))
                base_amount = sum(all_invl.mapped('price_subtotal'))
                this_amount = sum(this_invl.mapped('price_subtotal'))

                retention = o.base_amount * 0.1
                sheet.write(i, 0, o.sequence or '', bold)
                sheet.write(i, 1, o.percent, bold)
                sheet.write(i, 2, o.name, bold)
                sheet.write(i, 3, o.base_amount or 0.0, bold)
                sheet.write(i, 4, retention or '', bold)
                sheet.write(i, 5, o.approval_date or '', bold)
                sheet.write(i, 6, o.milestone_date or '', bold)
                sheet.write(i, 7, o.invoice_date or '', bold)
                sheet.write(i, 8, base_amount or 0.0, bold)
                sheet.write(i, 9, prev_amount or 0.0, bold)
                sheet.write(i, 10, this_amount or 0.0, bold)
                i += 1
                total_base_amount += base_amount
                total_next_amount += this_amount
                total_previous_amount += prev_amount
                total_retention += retention
                total_invoice_amount += this_amount
                if (not o.invoice_line_ids.mapped('invoice_id') in
                        invoice_residual_included):
                    invoice_residual_included.append(
                        o.invoice_line_ids.mapped('invoice_id'))
                    total_amount_residual += o.amount_residual
        else:
            for o in milestones:
                retention = o.base_amount * 0.1
                sheet.write(i, 0, o.sequence or '', bold)
                sheet.write(i, 1, o.percent, bold)
                sheet.write(i, 2, o.name, bold)
                sheet.write(i, 3, o.base_amount or 0.0, bold)
                sheet.write(i, 4, retention or '', bold)
                sheet.write(i, 5, o.approval_date.strftime(DT) or '', bold)
                sheet.write(i, 6, o.milestone_date.strftime(DT) or '', bold)
                sheet.write(i, 7, o.invoice_date.strftime(DT) or '', bold)
                sheet.write(i, 8, o.invoice_amount or 0.0, bold)
                sheet.write(i, 9, o.previous_amount or 0.0, bold)
                sheet.write(i, 10, o.next_amount or 0.0, bold)
                i += 1
                total_base_amount += o.base_amount
                total_next_amount += o.next_amount
                total_previous_amount += o.previous_amount
                total_retention += retention
                total_invoice_amount += o.invoice_amount
                if (not o.invoice_line_ids.mapped('invoice_id') in
                        invoice_residual_included):
                    invoice_residual_included.append(
                        o.invoice_line_ids.mapped('invoice_id'))
                    total_amount_residual += o.amount_residual

        i += 2

        sheet.write(i, 2, 'TOTAL CONTRACT', subtotal_style)
        sheet.write(i, 3, total_base_amount or '', subtotal_style)
        sheet.write(i, 4, total_retention or '', subtotal_style)
        sheet.write(i, 5, '', subtotal_style)
        sheet.write(i, 6, '', subtotal_style)
        sheet.write(i, 7, '', subtotal_style)
        sheet.write(i, 8, '', subtotal_style)
        sheet.write(i, 9, '', subtotal_style)
        sheet.write(i, 10, '', subtotal_style)
        i += 2

        sheet.write(i, 2, 'PREVIOUS REQUESTS', subtotal_style)
        sheet.write(i, 3, '', subtotal_style)
        sheet.write(i, 4, '', subtotal_style)
        sheet.write(i, 5, '', subtotal_style)
        sheet.write(i, 6, '', subtotal_style)
        sheet.write(i, 7, '', subtotal_style)
        sheet.write(i, 8, '', subtotal_style)
        sheet.write(i, 9, total_previous_amount, subtotal_style)
        sheet.write(i, 10, '', subtotal_style)
        i += 2

        received = total_previous_amount - total_amount_residual
        sheet.write(i, 2, 'RECEIVED TO DATE', subtotal_style)
        sheet.write(i, 3, '', subtotal_style)
        sheet.write(i, 4, '', subtotal_style)
        sheet.write(i, 5, '', subtotal_style)
        sheet.write(i, 6, '', subtotal_style)
        sheet.write(i, 7, '', subtotal_style)
        sheet.write(i, 8, received if received > 0.0 else 0.0, subtotal_style)
        sheet.write(i, 9, '', subtotal_style)
        sheet.write(i, 10, '', subtotal_style)

        i += 2

        sheet.write(i, 2, 'AMOUNT THIS INVOICE', subtotal_style)
        sheet.write(i, 3, '', subtotal_style)
        sheet.write(i, 4, '', subtotal_style)
        sheet.write(i, 5, '', subtotal_style)
        sheet.write(i, 6, '', subtotal_style)
        sheet.write(i, 7, '', subtotal_style)
        sheet.write(i, 8, '', subtotal_style)
        sheet.write(i, 9, '', subtotal_style)
        sheet.write(i, 10, total_next_amount, subtotal_style)

        i += 2

        sheet.write(i, 2, 'AMOUNT OWED', subtotal_style)
        sheet.write(i, 3, '', subtotal_style)
        sheet.write(i, 4, '', subtotal_style)
        sheet.write(i, 5, '', subtotal_style)
        sheet.write(i, 6, '', subtotal_style)
        sheet.write(i, 7, '', subtotal_style)
        sheet.write(i, 8, total_amount_residual, subtotal_style)
        sheet.write(i, 9, '', subtotal_style)
        sheet.write(i, 10, '', subtotal_style)

        i += 2

        sheet.write(i, 2, 'TOTAL AMOUNT BASE', total_style)
        sheet.write(i, 3, total_base_amount or '', total_style)
        sheet.write(i, 4, total_retention or '', total_style)
        sheet.write(i, 5, '', total_style)
        sheet.write(i, 6, '', total_style)
        sheet.write(i, 7, '', total_style)
        sheet.write(i, 8, total_invoice_amount, total_style)
        sheet.write(i, 9, total_previous_amount, total_style)
        sheet.write(i, 10, total_next_amount, total_style)
