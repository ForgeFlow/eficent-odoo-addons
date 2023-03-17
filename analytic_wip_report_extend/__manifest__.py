# Copyright 2023 ForgeFlow S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


{
    "name": "Work In Progress Statement Extend",
    "version": "14.0.1.0.0",
    "author": "ForgeFlow",
    "category": "Projects",
    "summary": """This adds new fields to analytic wip statement report""",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "license": "",
    "depends": [
        "analytic_wip_report",
        "account_analytic_parent",
    ],
    "data": ["views/account_analytic_account_view.xml"],
    "installable": True,
    "auto_install": True,
}
