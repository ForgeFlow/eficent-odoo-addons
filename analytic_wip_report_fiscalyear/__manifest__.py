# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Work In Progress Statement Fiscal Year",
    "version": "12.0.1.0.0",
    "author": "Eficent, Odoo Community Association (OCA), "
    "Project Expert Team",
    "website": "http://project.expert",
    "category": "Project Management",
    "license": "AGPL-3",
    "depends": ["analytic_wip_report", "account_fiscal_year"],
    "data": [
        "views/account_analytic_account_view.xml",
        "wizards/analytic_wip_report_view.xml",
    ],
    "installable": True,
}
