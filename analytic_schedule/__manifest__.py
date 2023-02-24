# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Analytic Schedule",
    "version": "14.0.1.0.0",
    "summary": "Automatically computes start and end dates for analytic "
    "accounts based on the earliest start and latest finish date "
    "of the children.",
    "author": "ForgeFlow",
    "license": "AGPL-3",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "category": "Generic Modules/Projects & Services",
    "depends": ["project", "analytic", "account_analytic_parent"],
    "data": ["views/analyltic_account_view.xml"],
    "installable": True,
}
