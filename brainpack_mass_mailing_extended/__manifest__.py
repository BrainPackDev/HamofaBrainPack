{
    'name': 'BrainPack Mass Mailing Extended',
    'version': '16.0.0.0',
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    'license': 'LGPL-3',
    'sequence': 2,
    'images': [],
    'summary': """
    """,
    'depends': ['mass_mailing','mass_mailing_themes'],
    'data': [
        'views/mass_mailing_themes_templates.xml'
    ],
    'assets': {
        'web.assets_frontend': [
        ],
        'web.assets_backend': [
            '/brainpack_mass_mailing_extended/static/src/js/mailing_mailing_view_form_full_width.js',

        ],
        'mass_mailing.assets_mail_themes_edition': [
            '/brainpack_mass_mailing_extended/static/src/css/style.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """
    """,
}