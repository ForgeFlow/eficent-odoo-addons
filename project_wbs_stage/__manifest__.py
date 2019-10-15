# Copyright 2017-19 Eficent Business and IT Consulting Services S.L.
# Copyright 2017-19 Luxim d.o.o.
# Copyright 2017-19 Matmoz d.o.o.
# Copyright 2017-19 Deneroteam.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Project WBS Stage",
    "version": "12.0.1.0.0",
    "author": "Eficent",
    'license': "LGPL-3",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "summary": """Add the stage to the project wbs
    """,
    "depends": ["project_wbs", "analytic", "base_kanban_stage"],
    "data": [
        "views/account_analytic_account_view.xml",
        "views/project_project_view.xml",
    ],

    'installable': True,
}
