import logging

from odoo import models, fields, api
from odoo.tools import populate, groupby

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = "crm.lead"

    tracking_emails_count = fields.Integer(
        compute="_compute_partner_id", readonly=True
    )

    def _compute_partner_id(self):
        partners_mail = self.partner_id.filtered("email")
        mt_obj = self.env["mail.tracking.email"].sudo()
        tracking_emails_count = 0
        if partners_mail.email:
            tracking_emails_count = tracking_emails_count + len(
                mt_obj.search([("recipient_address", "=", partners_mail.email.lower()),('mail_message_id.res_id','=',str(self.id)),('mail_message_id.model','=','crm.lead')])
            )
        self.tracking_emails_count = tracking_emails_count

    def open_mail_tracking_form(self):
        partners_mail = self.partner_id.filtered("email")
        mt_obj = self.env["mail.tracking.email"].sudo()
        if partners_mail.email:
            mt_obj = mt_obj.search(
                [("recipient_address", "=", partners_mail.email.lower()), ('mail_message_id.res_id', '=', str(self.id)),
                 ('mail_message_id.model', '=', 'crm.lead')])
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