# -*- coding: utf-8 -*-
import logging
from odoo import _, fields, models
from odoo.addons.base.models.ir_mail_server import MailDeliveryException

_logger = logging.getLogger(__name__)


class IrMailServer(models.Model):
    """Represents an SMTP server, able to send outgoing emails, with SSL and TLS capabilities."""
    _inherit = "ir.mail_server"
    company_id = fields.Many2one('res.company', 'Company', required=False)


class MailMail(models.Model):
    _inherit = "mail.mail"

    def send(self, auto_commit=False, raise_exception=False):
        """ Sends the selected emails immediately, ignoring their current
            state (mails that have already been sent should not be passed
            unless they should actually be re-sent).
            Emails successfully delivered are marked as 'sent', and those
            that fail to be deliver are marked as 'exception', and the
            corresponding error mail is output in the server logs.

            :param bool auto_commit: whether to force a commit of the mail status
                after sending each mail (meant only for scheduler processing);
                should never be True during normal transactions (default: False)
            :param bool raise_exception: whether to raise an exception if the
                email sending process has failed
            :return: True
        """
        for mail_server_id, smtp_from, batch_ids in self._split_by_mail_configuration():
            smtp_session = None
            # NTD
            comp_id = self.env.company.id
            mail_server_id = self.env['ir.mail_server'].search([('company_id', '=', comp_id)], limit=1)
            if mail_server_id:
                try:
                    smtp_session = self.env['ir.mail_server'].connect(mail_server_id=mail_server_id.id, smtp_from=smtp_from)

                except Exception as exc:
                    if raise_exception:
                        # To be consistent and backward compatible with mail_mail.send() raised
                        # exceptions, it is encapsulated into an Odoo MailDeliveryException
                        raise MailDeliveryException(_('Unable to connect to SMTP Server'), exc)
                    else:
                        batch = self.browse(batch_ids)
                        batch.write({'state': 'exception', 'failure_reason': exc})
                        batch._postprocess_sent_message(success_pids=[], failure_type="mail_smtp")
                else:
                    self.browse(batch_ids)._send(
                        auto_commit=auto_commit,
                        raise_exception=raise_exception,
                        smtp_session=smtp_session)
                    _logger.info(
                        'Sent batch %s emails via mail server ID #%s',
                        len(batch_ids), mail_server_id)
                finally:
                    if smtp_session:
                        smtp_session.quit()
            # else:
            #     raise MailDeliveryException(_('Mail not sent'), Exception)
