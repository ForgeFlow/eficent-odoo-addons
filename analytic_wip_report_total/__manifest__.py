# Copyright 2023 ForgeFlow S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

{
    "name": "Totals in analytic wip report view",
    "version": "15.0.1.0.0",
    "author": "ForgeFlow",
    "category": "Projects",
    "summary": """Add the totals in tree view""",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "license": "LGPL-3",
    "depends": [
        "analytic_wip_report_extend",
    ],
    "data": [
        "views/wip_report_view.xml",
    ],
    "installable": True,
}
