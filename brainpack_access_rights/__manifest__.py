# -*- coding: utf-8 -*-
{
    'name': "BrainPack Access Rights",

    'summary': """
      """,

    'author': "BrainPack",
    'website': "https://www.brainpack.io",
    'category': 'Uncategorized',
    'version': '16.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['web','base'],

    'data': [
        'security/res_group.xml',
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/ir_module_views.xml',
        'views/menu.xml',
        'wizard/get_app_message.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/brainpack_access_rights/static/src/js/form_controller.js',
            '/brainpack_access_rights/static/src/js/settings_form_controller.js',
            # '/brainpack_access_rights/static/src/js/systray_item.js',
            '/brainpack_access_rights/static/src/js/group_by_menu.js',
            '/brainpack_access_rights/static/src/js/filter_menu.js',
        ],
    },

}
