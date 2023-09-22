{
    "name": "Website Helpdesk Mgmt",
    "version": "15.0.1.0.0",
    "category": "After-Sales",
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    "depends": ["helpdesk_mgmt", "website"],
    "installable": True,
    "data": ["data/ir_model_data.xml","views/helpdesk_templates.xml"],
    'assets': {
        'website.assets_editor': [
            '/website_helpdesk_mgmt/static/src/js/website_form_project_editor.js',
        ],
    },
}
