# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Analytic Milestones',
    'version': '12.0.1.0.0',
    'author': 'ForgeFlow, ',
    'website': 'https://www.forgeflow.com',
    'category': 'Projects',
    'license': 'AGPL-3',
    'depends': [
        'project_wbs',
        'report_xlsx',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_analytic_milestone_view.xml',
        'views/account_analytic_account_view.xml',
        'views/account_invoice_view.xml',
        'wizards/analytic_milestone_change_state_view.xml',
        'wizards/analytic_milestone_view.xml',
        'wizards/analytic_milestone_invoice_process.xml',
        'report/analytic_milestone_xlsx.xml',
    ],
    'installable': True,
}
