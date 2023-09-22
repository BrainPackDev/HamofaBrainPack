from odoo import api, http, fields, models, tools

class ModuleInherit(models.Model):
    _inherit = "ir.module.module"

    def button_get_app(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Message',
            'res_model': 'get.app.messsage',
            'view_mode': 'form',
            'target': 'new',
        }
