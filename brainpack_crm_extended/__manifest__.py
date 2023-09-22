{
    'name': 'BrainPack CRM',
    'version': '16.0.0.1',
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    'license': 'LGPL-3',
    'sequence': 2,
    'images': [],
    'summary': """
    """,
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_view.xml',
        'views/investment_amount.xml',
        'views/lead_status_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/brainpack_crm_extended/static/src/css/style.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """
    """,
}