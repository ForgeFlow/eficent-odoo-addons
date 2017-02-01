# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Manage Locations for projects',
    'version': '7.0.1.0.0',
    'category': 'Logistics',
    'summary': 'Manage Locations for projects',
    'description': """
    Manage Locations for projects
""",
    'author': 'Eficent',
    'website': 'http://www.eficent.com',
    'depends': ['stock', 'analytic', 'stock_location_analytic'],
    'data': ['wizard/analytic_location_manager.xml'],
    'installable': True,
    'auto_install': False,
}
