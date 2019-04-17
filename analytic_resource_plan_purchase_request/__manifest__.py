# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.

{
    'name': 'Analytic Resource Planning - Purchase Requests',
    'version': '10.0.1.0.1',
    'author':   'Eficent, Odoo Community Association (OCA),'
                'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': [
        'analytic_resource_plan_stock',
        'analytic_location',
        'purchase_request'
    ],
    'data': [
        'views/purchase_request_view.xml',
        'views/analytic_resource_plan_view.xml',
        'wizard/analytic_resource_plan_line_make_purchase_request.xml',
    ],
    'installable': True,
}
