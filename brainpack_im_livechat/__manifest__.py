# -*- coding: utf-8 -*-
{
    'name': "BrainPack Live Chat",

    'summary': """
      """,

    'author': "BrainPack",
    'website': "https://www.brainpack.io",
    'category': 'Uncategorized',
    'version': '16.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','im_livechat'],

    'data': [
        'views/im_livechat_channel_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
        ],
    },

}
