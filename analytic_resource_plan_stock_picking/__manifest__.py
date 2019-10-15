# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Analytic Resource Planning - get resources",
    "version": "12.0.1.0.0",
    "author": "Eficent",
    "license": "AGPL-3",
    "website": "www.eficent.com",
    "summary": """Fetch stock for projects""",
    "category": "Generic Modules/Projects & Services",
    "depends": [
        "project_location",
        "analytic_resource_plan_purchase_request",
        "analytic_resource_plan",
        "analytic_resource_plan_stock",
    ],
    "data": [
        "views/stock_picking_view.xml",
        "views/analytic_resource_plan_view.xml",
        "wizard/delivery.xml",
    ],
    "installable": True,
}
