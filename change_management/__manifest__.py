# -*- coding: utf-8 -*-
# Copyright 2017 Matmoz d.o.o. (<http://www.matmoz.si>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Change Management',
    'version': '10.0.1.0.0',
    'author': 'Matmoz d.o.o., Odoo Community Association (OCA),'
              'Project Expert Team',
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'summary': 'Change Management integrated with Stakeholders Requirements',
    'depends': [
        'project',
        'project_wbs'
    ],
    'data': [
        'data/change_management_data.xml',
        'data/change_management_sequence.xml',
        'security/ir.model.access.csv',
        'view/project_task_view.xml',
        'view/change_management_view.xml',
        'view/change_management_category_view.xml',
        'view/change_management_proximity_view.xml',
        'view/change_management_menus.xml'
    ],
    'demo': [
        'demo/change_management_demo.xml'
    ],
    #    'test': ['test/test_change_management.yml'],
    'installable': True,
    'application': True,
}
