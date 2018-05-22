# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Stock Location Analytic',
    'version': '7.0.1.0.0',
    'category': 'Logistics',
    'summary': 'Introduces the analytic account to the locations',
    'description': """
    Introduces the analytic account to the locations.
    This allows to have dedicated locations for projects. This is useful when
    adding the analytic account to stock moves.
""",
    'author': 'Eficent',
    'website': 'http://www.eficent.com',
    'depends': ['stock', 'analytic', 'analytic_location'],
    'data': ['views/stock_view.xml'],
    'demo': ['demo/stock_data.xml'],
    'installable': True,
    'auto_install': False,
}
