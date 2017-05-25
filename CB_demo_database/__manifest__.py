# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Creu Blanca Demo Database',
    'summary': '',
    'version': '10.0.1.0.0',
    'author': 'Eficent, Odoo Community Association (OCA)',
    'category': '',
    'depends': [
        'medical_careplan',
        'workflow_plandefinition',
    ],
    'demo': [
        'demo/workflow_types_demo.xml',
        'demo/activity_definitions_demo.xml',
        'demo/plan_definition_demo.xml',
        'demo/careplan_demo.xml',
    ],
    'website': '',
    'licence': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}
