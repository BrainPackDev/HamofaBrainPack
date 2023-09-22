# -*- coding: utf-8 -*-
{
    'name': 'Brainpack Search View On Discuss App',
    'category': 'Discuss',
    'summary': 'Search View On Discuss App',
    'author': "BrainPack",
    'website': "https://www.brainpack.io",
    'category': 'Discuss',
    'version': '16.0.0.0',
    # any module necessary for this one to work correctly
    'depends': ['mail','brainpack_meta_whatsapp_discuss'],
    'data': [

    ],
    'assets': {
        'web.assets_backend': [
            # 'https://cdn.jsdelivr.net/mark.js/8.6.0/jquery.mark.min.js',
            'brainpack_discuss_search_view_cr/static/src/js/mark.min.js',
            'brainpack_discuss_search_view_cr/static/src/js/thread_view_nav.js',
            'brainpack_discuss_search_view_cr/static/src/js/discuss_sidebar_category_item.js',
            'brainpack_discuss_search_view_cr/static/src/js/message.js',
            'brainpack_discuss_search_view_cr/static/src/js/discuss.js',
            'brainpack_discuss_search_view_cr/static/src/js/messaging_notification_handler.js',
            'brainpack_discuss_search_view_cr/static/src/js/thread_cache.js',
            'brainpack_discuss_search_view_cr/static/src/js/thread.js',
            'brainpack_discuss_search_view_cr/static/src/js/thread_view.js',
            'brainpack_discuss_search_view_cr/static/src/js/thread_viewer.js',
            'brainpack_discuss_search_view_cr/static/src/js/discuss_container.js',
            'brainpack_discuss_search_view_cr/static/src/js/message_component.js',
            'brainpack_discuss_search_view_cr/static/src/js/thread_view_component.js',
            'brainpack_discuss_search_view_cr/static/src/xml/discuss_container.xml',
            'brainpack_discuss_search_view_cr/static/src/xml/thread_view.xml',
            'brainpack_discuss_search_view_cr/static/src/xml/message.xml',
            'brainpack_discuss_search_view_cr/static/src/css/style.css',
        ],
    },

}
