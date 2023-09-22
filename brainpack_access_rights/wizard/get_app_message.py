from odoo import api, http, fields, models, tools

class GetAppMessage(models.TransientModel):
    _name = 'get.app.messsage'
    _description = 'Get App Message'

    name = fields.Char(
        string='Name',
        readonly=True)

    def contact_us(self):
        return {
            'type': 'ir.actions.act_url',
            'url': self.env.company.support_url if self.env.company and self.env.company.support_url else 'https://www.brainpack.io/support',
            'target': 'new',
        }