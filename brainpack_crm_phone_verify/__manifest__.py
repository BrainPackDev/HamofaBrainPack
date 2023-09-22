{
    'name': 'BrainPack Phone Automation',
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
            '/brainpack_crm_phone_verify/static/src/phone_field/phone_field.js',
            '/brainpack_crm_phone_verify/static/src/phone_field/VerifyPhoneField.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """
    """,
}