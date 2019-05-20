# Copyright 2017-19 Eficent Business and IT Consulting Services S.L.
# Copyright 2017-19 Luxim d.o.o.
# Copyright 2017-19 Matmoz d.o.o.
# Copyright 2017-19 Deneroteam.

# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Project WBS Stage",
    "version": "12.0.1.0.0",
    "author": "Eficent",
    'license': "AGPL-3",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "summary": """Add the stage to the project wbs
    """,
    "depends": ["project_wbs", "analytic", "project"],
    "data": [
        "views/analytic_account_stage_view.xml",
        "views/account_analytic_account_view.xml",
        "views/project_project_view.xml",
        "security/ir.model.access.csv",
    ],

    'installable': True,
}
