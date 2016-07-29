# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Partner External Reference",
    "summary": "Adds external references to partners",
    "version": "9.0.1.0.0",
    "category": "Generic Modules",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "https://www.odoo-community.org",
    "license": "LGPL-3",
    "depends": ['base'],
    "data": [
        'security/ir.model.access.csv',
        'views/partner_external_reference_origin_view.xml',
        'views/partner_external_reference_view.xml',
        'views/res_partner_view.xml',
    ],
    "installable": True,
}

