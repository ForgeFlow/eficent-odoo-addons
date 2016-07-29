# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Project WBS Element',
    'summary': 'Manage Work Breakdown Structures in your Projects',
    'version': '9.0.1.0.0',
    'author': 'Eficent Business and IT Consulting Services S.L.,'
    'Odoo Community Association (OCA)',
    'website': 'https://www.odoo-community.org',
    'category': 'Warehouse Management',
    'license': 'AGPL-3',
    'depends': [
        'project',
    ],
    'data': [
        'views/project_task_view.xml',
        'views/project_wbs_element_view.xml',
        'views/project_view.xml',
    ],
    'installable': True,
    'active': False,
}
