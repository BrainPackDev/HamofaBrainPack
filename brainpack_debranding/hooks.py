from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _

def pre_init_hook(cr):
    try:
        sql = "UPDATE ir_module_module SET website = '%s' WHERE license like '%s' and website <> ''" % ('https://www.brainpack.io', 'OEEL%')
        cr.execute(sql)
        cr.commit()
    except Exception as e:
        pass

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    moduless = env['ir.module.module'].search([])
    for module in moduless:
        module.icon_image = ''
        if module.id:
            path = modules.module.get_module_icon(module.name)
        else:
            path = ''
        if path:
            module.write({'icon': path})

