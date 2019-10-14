# Copyright 2015-19 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Request Sale",
    "version": "12.0.1.0.0",
    "author": "Eficent",
    'license': 'AGPL-3',
    "website": "www.eficent.com",
    "category": "Purchase Management",
    "depends": ["purchase_request", "sale"],
    "summary": """
        Link from sales to Purchase Requests
    """,
    "data": [
        "views/purchase_request_view.xml"
    ],
    'installable': True,
}
