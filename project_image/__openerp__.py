# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Project Image',
    'summary': 'Adds a default image to the project Kanban view',
    'version': '9.0.1.0.0',
    'category': 'Generic Modules',
    'author': 'Eficent Business and IT Consulting Services S.L., '
              'Odoo Community Association (OCA)',
    'website': 'https://www.odoo-community.org',
    'license': 'LGPL-3',
    'depends': ['project'],
    'data': [
        'views/project_view.xml',
    ],
    'installable': True,
}
