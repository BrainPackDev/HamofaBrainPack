from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class Components(models.Model):
    _name = "components"
    _description = 'Whatsapp Components'

    type = fields.Selection([('header', 'HEADER'),
                            ('body', 'BODY'),
                            ('footer', 'FOOTER')],
                            'Type', default='header')
    formate = fields.Selection([('text', 'TEXT'),
                            ('media', 'MEDIA')],
                            'Formate', default='text')

    media_type = fields.Selection([('document', 'DOCUMENT'),
                            ('video', 'VIDEO'),
                            ('image', 'IMAGE'),],
                            'Media Type', default='document')

    text = fields.Text('Text')

    variables_ids = fields.One2many('variables','component_id','Variables')
    wa_template_id = fields.Many2one('wa.template')
    model_id = fields.Many2one('ir.model')

    @api.onchange("text")
    def onchange_text(self):
        for rec in self:
            if rec.type == 'header' and rec.formate == 'text' and rec.text and len(rec.text) > 60:
                raise UserError(_("60-character limit for headers text."))
            if rec.type == 'body' and rec.formate == 'text' and rec.text and len(rec.text) > 1024:
                raise UserError(_("1,024-character limit for body text."))

    @api.constrains('type', 'formate', 'text')
    def _constrain_text_length(self):
        for rec in self:
            if rec.type == 'header' and rec.formate == 'text' and rec.text and len(rec.text) > 60:
                raise UserError(_("60-character limit for headers text."))
            if rec.type == 'body' and rec.formate == 'text' and rec.text and len(rec.text) > 1024:
                raise UserError(_("1,024-character limit for body text."))

