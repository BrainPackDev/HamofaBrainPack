{
    'name': 'BrainPack Logo on Login',
    'version': '16.0.0.0',
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    'license': 'LGPL-3',
    'sequence': 2,
    'images': [],
    'summary': """
    """,
    'depends': ['website'],
    'data': [
        'views/login.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'brainpack_logo_on_login/static/src/css/style.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """
    """,
}