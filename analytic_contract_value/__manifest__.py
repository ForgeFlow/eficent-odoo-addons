# Copyright 2015-23 ForgeFlow S.L.
# Copyright 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Analytic Contract Value",
    "version": "14.0.1.0.0",
    "summary": "Sets a Contract Value on the analytic account",
    "author": "ForgeFlow",
    "license": "AGPL-3",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "category": "Generic",
    "depends": ["analytic", "analytic_plan"],
    "data": [
        "security/analytic_security.xml",
        "views/analytic_account_view.xml",
    ],
    "installable": True,
}
