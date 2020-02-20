{
    'name': 'Analytic Resource Plan Stock',
    'version': '12.0.1.0.0',
    'author': 'Eficent, '
    'Matmoz, '
    'Luxim, '
    'Project Expert Team',
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'summary': 'Stock on Resource Plan',
    'depends': [
        'analytic_resource_plan',
        'stock_location_analytic',
        'stock_analytic_account',
    ],
    'data': [
        'views/analytic_resource_plan_line_view.xml'
    ],
    'installable': True,
}
