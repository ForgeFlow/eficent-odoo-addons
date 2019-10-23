# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Project Cost Category",
    "version": "12.0.1.0.0",
    "summary": """Adds the cost category to projects.""",
    "author": "Eficent, Odoo Community Association (OCA)",
    "website": "http://www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "license": "AGPL-3",
    "depends": ["project", "account_analytic_cost_category"],
    "data": ["views/project_view.xml"],
    "installable": True,
}
