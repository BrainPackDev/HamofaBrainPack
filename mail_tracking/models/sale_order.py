import logging

from odoo import models, fields, api
from odoo.tools import populate, groupby

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    tracking_emails_count = fields.Integer(
        compute="_compute_partner_id", readonly=True
    )

    def _compute_partner_id(self):
        partners_mail = self.partner_id.filtered("email")
        mt_obj = self.env["mail.tracking.email"].sudo()
        tracking_emails_count = 0
        for partner in partners_mail:
            tracking_emails_count = tracking_emails_count + len(
                mt_obj.search([("recipient_address", "=", partner.email.lower()),('mail_message_id.res_id','=',str(self.id)),('mail_message_id.model','=','sale.order')])
            )
        self.tracking_emails_count = tracking_emails_count

    def open_mail_tracking_form(self):
        partners_mail = self.partner_id.filtered("email")
        mt_obj = self.env["mail.tracking.email"].sudo()
        if partners_mail:
            mt_obj = mt_obj.search(
                [("recipient_address", "=", partners_mail.email.lower()), ('mail_message_id.res_id', '=', str(self.id)),
                 ('mail_message_id.model', '=', 'sale.order')])
        return {
            'name': ('MailTracking emails'),
            'view_mode': 'tree,form',
            'target': 'current',
            'res_model': 'mail.tracking.email',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', mt_obj.ids)],
            'context': {
            }
        }