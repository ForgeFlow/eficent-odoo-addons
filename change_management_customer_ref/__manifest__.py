# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Change Management Customer Reference',
    'version': '12.0.1.0.0',
    'author': 'Eficent Business and IT Consulting Services S.L.',
    'website': 'www.eficent.com',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'summary': 'Creates the customer and Change code',
    'depends': [
        'change_management'
    ],
    'data': [
        'views/change_management_view.xml',
    ],
    'installable': True,
    'application': True,
}
