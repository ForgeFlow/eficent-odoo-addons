# Copyright 2014-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Analytic Resource Plan MRP",
    "version": "10.0.1.0.0",
    "summary": """Analytic Resource Plan MRP""",
    "author": "Eficent, Odoo Community Association (OCA)",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "license": "AGPL-3",
    "category": "Generic Modules/Projects & Services",
    "depends": [
        "analytic_resource_plan_stock",
        "mrp",
        "analytic_location",
    ],
    "data": [
        "wizard/consume_view.xml",
        "wizard/produce_view.xml",
        "views/analytic_resource_plan_line_view.xml",
    ],
    "installable": True,
}
