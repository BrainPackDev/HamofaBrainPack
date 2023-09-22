# -*- coding: utf-8 -*-
# Developed by Bizople Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details

from odoo import api, models
from odoo.http import request

class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        # Show company change option even if single company available 
        res = super(Http, self).session_info()
        user = request.env.user
        company = request.env.company

        if self.env.user.has_group('base.group_user'):
            res.update({
                "display_switch_company_menu": True,
                "prevent_auto_save_warning_msg": company.prevent_auto_save_warning if company.prevent_auto_save_warning else '',
            })
        return res