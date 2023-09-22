{
    'name': 'BrainPack Website Extended',
    'version': '16.0.0.0',
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    'license': 'LGPL-3',
    'sequence': 2,
    'images': [],
    'summary': """
    """,
    'depends': ['website','website_crm','project'],
    'data': [
        'views/snippet.xml',
        'views/crm_lead.xml',
        'views/project_task.xml',
    ],
    'assets': {
            'web.assets_frontend': [
                # '/brainpack_website_extended/static/src/js/lightslider.js',
                '/brainpack_website_extended/static/src/js/snippet.js',
                '/brainpack_website_extended/static/src/js/portal.js',
                '/brainpack_website_extended/static/src/js/s_website_form.js',
                # '/brainpack_website_extended/static/src/css/lightslider.css',
                '/brainpack_website_extended/static/src/css/style.css',
                '/brainpack_website_extended/static/src/css/rubik.css',
                '/brainpack_website_extended/static/src/css/notosans.css',
                '/brainpack_website_extended/static/src/css/style.scss',
            ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """
    """,
}