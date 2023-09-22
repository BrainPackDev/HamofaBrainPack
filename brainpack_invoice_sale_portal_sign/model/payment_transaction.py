from odoo import api, fields, models


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _finalize_post_processing(self):
        super()._finalize_post_processing()
        self.invoice_ids.action_invoice_sign_mail_template()
