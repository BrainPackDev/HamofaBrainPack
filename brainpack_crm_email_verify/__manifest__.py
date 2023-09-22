{
    'name': 'BrainPack Email Automation',
    'version': '16.0.0.1',
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    'license': 'LGPL-3',
    'sequence': 2,
    'images': [],
    'summary': """
    """,
    'depends': ['brainpack_crm_extended'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_view.xml',
        'wizard/reason_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/brainpack_crm_email_verify/static/src/email_field/email_field.js',
            '/brainpack_crm_email_verify/static/src/email_field/VerifyEmailField.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """
    """,
}