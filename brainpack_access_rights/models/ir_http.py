# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models
from odoo.http import request

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super(IrHttp, self).session_info()
        config_parameter = request.env['ir.config_parameter'].sudo()
        result['main_admin'] = self.env.user and self.env.user.has_group('brainpack_access_rights.main_admin')
        result['field_lst'] = self.env.company and self.env.company.sudo().field_ids.mapped('name')
        result['menu_lst'] = self.env.company and self.env.company.sudo().modules_ids.mapped('name')
        result['brainpack_support_url'] = self.env.company.support_url if self.env.company and self.env.company.support_url else 'https://www.brainpack.io/support'
        result['module_action_id'] = self.env.ref('base.open_module_tree').id
        return result
