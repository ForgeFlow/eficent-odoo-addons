# © 2014-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Project Manufacturing Order Link",
    "version": "12.0.1.0.0",
    "author": "Eficent",
    "license": "AGPL-3",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["project", "mrp_analytic"],
    "summary": """
            Project Manufacturing Order Link
    """,
    "data": [
        "view/project_view.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True,

}
