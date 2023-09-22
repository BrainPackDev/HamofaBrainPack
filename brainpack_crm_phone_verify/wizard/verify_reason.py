from odoo import api, http, fields, models, tools,_
AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]


class VerifyPhoneReason(models.TransientModel):
    _name = 'verify.phone.reason'
    _description = 'Verify Phone Reason'

    phone = fields.Char('Phone')
    phone_status = fields.Selection([
        ('answered', 'Answered'),
        ('not_answered', 'Not Answered'),
        ('out_of_service', 'Out Of Service'),
    ], string='Phone Status')
    message = fields.Text('Message')
    investment_amount_id = fields.Many2one('investment.amount', 'Investment Amount')
    case_type = fields.Selection([
        ('regulated_fx', 'Regulated FX'),
        ('unregulated_fx', 'Unregulated FX'),
        ('crypto', 'Crypto'),
    ], string='Case Type')
    date_deadline = fields.Date('Expected Closing', help="Estimate of the date on which the opportunity will be won.")
    transfer_type = fields.Selection([
        ('crypto_to_crypto', 'Crypto to crypto'),
        ('wire', 'Wire'),
        ('credit_card', 'Credit card'),
    ], string='Transfer Type')
    priority = fields.Selection(
        AVAILABLE_PRIORITIES, string='Priority', index=True,
        default=AVAILABLE_PRIORITIES[0][0])

    @api.onchange('phone_status')
    def _onchange_phone_status(self):
        for rec in self:
            if rec.phone_status in ['not_answered', 'out_of_service']:
                rec.case_type = False
                rec.message = False
                rec.investment_amount_id = False
                rec.date_deadline = False
                rec.transfer_type = False
                rec.priority = False

    @api.model
    def create(self,vals):
        res = super().create(vals)
        lead = self.env['crm.lead'].browse(self.env.context.get('active_id'))
        if lead:
            lead.write({
                'phone_status':res.phone_status,'case_type':res.case_type,'transfer_type':res.transfer_type,
                'investment_amount_id':res.investment_amount_id.id if res.investment_amount_id else False,
                'message':res.message,
                'date_deadline':res.date_deadline,
                'priority':res.priority,
            })
        return res

    def write(self, vals):
        res = super().write(vals)
        lead = self.env['crm.lead'].browse(self.env.context.get('active_id'))
        if lead:
            lead.write({
                'phone_status': self.phone_status, 'case_type': self.case_type, 'transfer_type': self.transfer_type,
                'investment_amount_id': res.investment_amount_id.id if res.investment_amount_id else False,
                'message': self.message,
                'date_deadline': self.date_deadline,
                'priority': self.priority,
            })
        return res


    def update_reason(self):
        return {
            'name': _('Schedule an Activity'),
            'context': {
                'default_res_id': self.env.context.get('active_id'),
                'default_res_model': 'crm.lead'
            },
            'view_mode': 'form',
            'res_model': 'mail.activity',
            'views': [(False, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }