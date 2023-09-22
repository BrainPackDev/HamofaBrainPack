from odoo import api, models, tools
import re

class MailMailInherit(models.Model):
    _inherit = "mail.mail"

    @api.model_create_multi
    def create(self, values_list):
        for vals in values_list:
            if 'subject' in vals and vals.get('subject'):
                vals.update({'subject':  re.sub(
                        r"""(Odoo)""", "BrainPack", vals.get('subject')
                    ) })
        res = super().create(values_list)
        return res