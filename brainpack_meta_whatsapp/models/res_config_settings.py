from odoo import api, fields, models,_


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_brainpack_meta_whatsapp_sale = fields.Boolean("Brainpack Whatsapp Sales")
    module_brainpack_meta_whatsapp_purchase = fields.Boolean("Brainpack Whatsapp Purchase")
    module_brainpack_meta_whatsapp_invoice = fields.Boolean("Brainpack Whatsapp Invoice")
    module_brainpack_meta_whatsapp_crm = fields.Boolean("Brainpack Whatsapp CRM")
    module_brainpack_meta_whatsapp_discuss = fields.Boolean("Brainpack Whatsapp Discuss")

    @api.onchange('module_brainpack_meta_whatsapp_crm')
    def on_module_tus_meta_wa_crm(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_meta_whatsapp_crm'.replace("module_", ''))])
        if not modules and self.module_brainpack_meta_whatsapp_crm:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Brainpack Whatsapp CRM module not exist!'),
                }
            }

    @api.onchange('module_brainpack_meta_whatsapp_discuss')
    def on_module_brainpack_meta_whatsapp_discuss(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_meta_whatsapp_discuss'.replace("module_", ''))])
        if not modules and self.module_tus_meta_wa_discuss:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Brainpack Whatsapp Discuss module not exist!'),
                }
            }

    @api.onchange('module_brainpack_meta_whatsapp_sale')
    def on_module_brainpack_meta_whatsapp_sale(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_meta_whatsapp_sale'.replace("module_", ''))])
        if not modules and self.module_brainpack_meta_whatsapp_sale:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Brainpack Whatsapp Sale module not exist!'),
                }
            }

    @api.onchange('module_brainpack_meta_whatsapp_purchase')
    def on_module_brainpack_meta_whatsapp_purchase(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_meta_whatsapp_purchase'.replace("module_", ''))])
        if not modules and self.module_brainpack_meta_whatsapp_purchase:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Brainpack Whatsapp Purchase module not exist!'),
                }
            }

    @api.onchange('module_brainpack_meta_whatsapp_invoice')
    def on_module_brainpack_meta_whatsapp_invoice(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_meta_whatsapp_invoice'.replace("module_", ''))])
        if not modules and self.module_brainpack_meta_whatsapp_invoice:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Brainpack Whatsapp Invoice module not exist!'),
                }
            }
