from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    phone_verify_reason = fields.Char('Verify Phone Reason',tracking=True)
    phone_status = fields.Selection([
        ('answered', 'Answered'),
        ('not_answered', 'Not Answered'),
        ('out_of_service', 'Out Of Service'),
    ], string='Phone Status', tracking=True, default='answered')
    case_type = fields.Selection([
        ('regulated_fx', 'Regulated FX'),
        ('unregulated_fx', 'Unregulated FX'),
        ('crypto', 'Crypto'),
    ], string='Case Type', tracking=True)
    transfer_type = fields.Selection([
        ('crypto_to_crypto', 'Crypto to crypto'),
        ('wire', 'Wire'),
        ('credit_card', 'Credit card'),
    ], string='Transfer Type', tracking=True)


