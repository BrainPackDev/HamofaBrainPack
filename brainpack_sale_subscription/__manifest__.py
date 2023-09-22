{
    'name': 'BrainPack Sale Subscription',
    'version': '16.0.0.0',
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    'license': 'LGPL-3',
    'sequence': 2,
    'images': [],
    'summary': """
    """,
    'depends': ['base','sale_subscription','brainpack_debranding','base_automation'],
    'data': [
        'data/data.xml',
        'views/brainpack_sale_subscription_views.xml',
        'views/sale_order.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """
    """,
}