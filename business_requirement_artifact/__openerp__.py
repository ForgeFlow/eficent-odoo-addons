# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# (https://www.eficent.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Business Requirement Artifact',
    'category': 'Business Requirements Management',
    'summary': 'Business Requirement',
    'version': '9.0.1.0.0',
    'website': 'www.eficent.com',
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Odoo Community Association (OCA)",
    'depends': [
        'business_requirement',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/artifact_view.xml',
        'views/business_view.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
}
