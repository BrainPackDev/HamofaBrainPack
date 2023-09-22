from odoo import _, api, fields, models, modules, tools

class Channel(models.Model):
    _inherit = 'mail.channel'

    whatsapp_channel = fields.Boolean(string="Whatsapp Channel")

    @api.constrains('channel_member_ids', 'channel_partner_ids')
    def _constraint_partners_chat(self):
        pass