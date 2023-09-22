{
    'name': 'Brainpack Meta Whatsapp Interactive Buttons',
    'version': '16.0',
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    'category': 'Base',
    'summary': 'Interactive Templates, Buttons send through brainpack on WhatsApp and Message Automation',
    'description': """
        Interactive Templates, Buttons send through odoo on WhatsApp and Message Automation
    """,
    'depends': ['brainpack_meta_whatsapp'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/components.xml',
    ],
    'installable': True,
    'auto_install': False,
}