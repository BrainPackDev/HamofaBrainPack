from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    app_system_name = fields.Char('System Name',default='BrainPack')

class BaseModel(models.AbstractModel):
    _inherit = 'base'

    def _notify_get_reply_to_formatted_email(self, record_email, record_name):
        if 'company_id' in self and len(self.company_id) == 1:
            record_email = self.sudo().company_id.email
        else:
            record_email = self.env.company.email
        return super()._notify_get_reply_to_formatted_email(record_email, record_name)
