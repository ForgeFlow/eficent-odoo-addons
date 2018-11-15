# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'MRP Location Analytic',
    'version': '7.0.1.0.0',
    'category': 'MRP',
    'summary': 'MRP using analytic locations',
    'description': """
    To manufacture for projects, use always the project location
""",
    'author': 'Eficent',
    'website': 'http://www.eficent.com',
    'depends': ['stock_location_analytic',
                'mrp_analytic',
                ],
    'data': [],
    'installable': True,
    'auto_install': False,
    
}
