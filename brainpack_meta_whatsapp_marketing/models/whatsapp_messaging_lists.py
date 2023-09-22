from odoo import models, api, fields

class WhatsAppMessagingLists(models.Model):
    _description = 'Whatsapp Messaging Lists'
    _name = 'whatsapp.messaging.lists'
    _rec_name = 'name'


    name = fields.Char('Name')
    contacts_ids = fields.Many2many('whatsapp.messaging.lists.contacts',string='Contacts')