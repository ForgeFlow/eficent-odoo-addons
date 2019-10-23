{
    "name": "Purchase Delivery Costs",
    "version": "12.0.1.0.0",
    "category": "Purchase Management",
    "summary": """Allows you to add delivery methods in purchase orders
    and pickings""",
    "author": "Eficent, Odoo Community Association (OCA)",
    "website": "www.eficent.com",
    "license": "AGPL-3",
    "depends": ["delivery", "purchase_analytic"],
    "data": ["view/purchase_view.xml", "view/delivery_view.xml"],
    "installable": True,
    "auto_install": False,
}
