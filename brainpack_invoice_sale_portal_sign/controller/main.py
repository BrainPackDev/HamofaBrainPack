import binascii

from odoo import http, _, fields
from odoo.http import request
from odoo.exceptions import AccessError, MissingError


class InvoiceSignature(http.Controller):

    @http.route(['/my/invoices/<int:invoice_id>/accept'], type='json', auth="public", website=True)
    def portal_invoice_sign(self, invoice_id, signature=None):
        try:
            invoice_sudo = request.env['account.move'].sudo().browse(invoice_id)
        except (AccessError, MissingError):
            return {'error': _('Invalid invoice.')}
        attachment = request.env['ir.attachment'].sudo().create({
            'name': invoice_sudo.name + '/' + invoice_sudo.partner_id.name + ' /Signature',
            'type': 'binary',
            'datas': signature
        })

        invoice_sudo.sudo().write({
            'signature_attachment': attachment.id
        })
        return {
            'force_refresh': True
        }

    @http.route(['/my/orders/<int:order_id>/sign'], type='json', auth="public", website=True)
    def portal_quote_accept(self, order_id, access_token=None, name=None, signature=None):
        try:
            order_sudo = request.env['sale.order'].sudo().browse(order_id)
        except (AccessError, MissingError):
            return {'error': _('Invalid order.')}

        try:
            order_sudo.sudo().write({
                'signed_by': name,
                'signed_on': fields.Datetime.now(),
                'signature': signature,
            })
            request.env.cr.commit()
        except (TypeError, binascii.Error) as e:
            return {'error': _('Invalid signature data.')}

        if not order_sudo._has_to_be_paid():
            order_sudo.sudo().action_confirm()
            order_sudo.sudo()._send_order_confirmation_mail()

        query_string = '&message=sign_ok'
        if order_sudo.sudo()._has_to_be_paid(True):
            query_string += '#allow_payment=yes'
        return {
            'force_refresh': True,
            'redirect_url': order_sudo.get_portal_url(query_string=query_string),
        }


