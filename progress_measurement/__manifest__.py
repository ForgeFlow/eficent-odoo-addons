# Copyright 2014-17 ForgeFlow S.L.
# Copyright 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Progress measurement",
    "version": "15.0.1.0.0",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "category": "Generic Modules",
    "depends": ["project"],
    "license": "AGPL-3",
    "summary": """
        Project degree of completion with respect
        to the estimated scope of work
    """,
    "data": [
        "views/progress_measurement_type_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
