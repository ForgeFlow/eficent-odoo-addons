# Copyright 2018-19 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Analytic Category",
    "summary": """
 Allow to define analytic categories for analytic accounts

    """,
    'license': 'AGPL-3',
    "version": "12.0.1.0.0",
    "author": "Eficent",
    "category": "Analytic",
    "depends": ["account"],
    "data": ["security/security.xml",
             "view/analytic_view.xml",
             "view/category_view.xml"],
    "installable": True
}
