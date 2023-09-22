from odoo import models, api, fields

class WhatsAppMessagingListsContacts(models.Model):
    _description = 'Whatsapp Messaging List Contacts'
    _name = 'whatsapp.messaging.lists.contacts'
    _rec_name = 'phone'

    name = fields.Char('Contact Name')
    phone = fields.Char('WhatsApp Number')