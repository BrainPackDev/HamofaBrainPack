# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re
from odoo.http import Response, request
from markupsafe import Markup

from odoo import api, models, tools

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super(IrHttp, self).session_info()
        config_parameter = request.env['ir.config_parameter'].sudo()

        result['app_system_name'] = self.env.company.app_system_name or 'BrainPack'

        # result['app_system_name'] = config_parameter.get_param('app_system_name', 'BrainPack')
        result['app_documentation_url'] = config_parameter.get_param('app_documentation_url')
        result['app_support_url'] = config_parameter.get_param('app_support_url')
        result['app_account_title'] = config_parameter.get_param('app_account_title')
        result['app_account_url'] = config_parameter.get_param('app_account_url')
        result['app_show_debug'] = config_parameter.get_param('app_show_debug')
        result['app_show_documentation'] = config_parameter.get_param('app_show_documentation')
        result['app_show_support'] = config_parameter.get_param('app_show_support')
        result['app_show_account'] = config_parameter.get_param('app_show_account')
        result['main_admin'] = self.env.user and self.env.user.has_group('brainpack_access_rights.main_admin')
        return result


def render(self):
    """ Renders the Response's template, returns the result. """
    self.qcontext['request'] = request

    if request.env["ir.ui.view"]._render_template(self.template, self.qcontext):
        message = tools.ustr(request.env["ir.ui.view"]._render_template(self.template, self.qcontext))
        wrapper = Markup if isinstance(message, Markup) else str
        view_rec = False
        if isinstance(self.template, int):
            view_rec = request.env['ir.ui.view'].sudo().search([('id','=',self.template)])
        if view_rec and view_rec.key == 'website.outsource':
            pass
        else:
            message = re.sub(
                r"""(Odoo)""", "BrainPack", message
            )
        return wrapper(message)

    return request.env["ir.ui.view"]._render_template(self.template, self.qcontext)
Response.render = render