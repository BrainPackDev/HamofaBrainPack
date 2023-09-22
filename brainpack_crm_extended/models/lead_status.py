from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _

class LeadStatus(models.Model):
    _name = 'lead.status'
    _description = 'Lead Status'
    _order = 'sequence, id'

    sequence = fields.Integer()
    name = fields.Char('Name')