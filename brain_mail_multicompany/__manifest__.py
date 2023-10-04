{
    "name": "Email Gateway Multi company",
    "version": "16.0.0.1.0",
    "category": "Extra Tools",
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    "license": "AGPL-3",
    "depends": ["mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/ir_mail_server_view.xml",
        "views/mail_server_view.xml",
        "views/alias_mail_view.xml",
     ],
    "installable": True,
}
