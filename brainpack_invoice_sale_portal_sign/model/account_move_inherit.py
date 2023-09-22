from odoo import fields, models, api


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    signature_attachment = fields.Many2one(
        comodel_name='ir.attachment',
        string="Attachments",
    )
    # signature_datas = fields.Binary(related='signature_attachment.datas',string="Signature")

    def action_invoice_sign_mail_template(self):
        mail_template = self.env.ref('brainpack_invoice_sale_portal_sign.invoice_sign_mail_template').id
        template = self.env['mail.template'].browse(mail_template)
        template.send_mail(self.id, force_send=True)
