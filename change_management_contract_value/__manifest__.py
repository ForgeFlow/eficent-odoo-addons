# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Change Management Contract Value',
    'version': '12.0.1.0.0',
    'author': 'Eficent Business and IT Consulting Services S.L.',
    'website': 'www.eficent.com',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'summary': 'Creates a project for each Change, child of the project '
               'indicated.',
    'depends': ['change_management_own_project', 'analytic_contract_value',
                'analytic_plan'],
    'data': [
        'security/ir.model.access.csv',
        'views/change_management_view.xml',
        'views/change_management_template_view.xml',
        'views/analytic_line_plan_view.xml',
    ],
    'installable': True,
}
