# © 2015-19 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Products Manufacturer Partner',
    'version': '12.0.1.0.0',
    'author': 'Eficent',
    "website": "www.eficent.com",
    "license": "LGPL-3",
    'category': 'Purchase Management',
    'summary': """
    Classify manufacturers by providing an indicator in the partner.
    In the product, select a manufacturer from the list of partners where
    this indicator has been set.
     """,
    'depends': [
        'purchase',
        'product_manufacturer'
    ],
    'data': [
        'view/partner_view.xml',
        'view/product_view.xml',
    ],
    'installable': True,
}
