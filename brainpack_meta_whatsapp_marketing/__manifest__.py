{
    'name': 'Brainpack Meta Whatsapp Marketing',
    'version': '1.0.',
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    'depends': ['brainpack_meta_whatsapp'],
    'data': [
        'security/ir.model.access.csv',
        'data/whatsapp_messaging_data.xml',
        'wizard/whatsapp_messaging_schedule_date_views.xml',
        'views/whatsapp_messaging_view.xml',
        'views/whatsapp_messaging_lists_view.xml',
        'views/whatsapp_messaging_lists_contacts_vies.xml',

    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
