# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Request Comment",
    "version": "14.0.1.0.0",
    "author": "ForgeFlow",
    "license": "AGPL-3",
    "website": "https://github.com/ForgeFlow/eficent-odoo-addons",
    "category": "Purchase Management",
    "depends": ["purchase_request_to_rfq", "purchase_comment_template"],
    "summary": """
        Link from sales to Purchase Requests
    """,
    "data": ["views/purchase_request_views.xml", "views/purchase_views.xml"],
    "installable": True,
}
