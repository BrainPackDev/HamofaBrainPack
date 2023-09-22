from odoo.http import request
from odoo.addons.mail.controllers.discuss import DiscussController
from odoo import http, _
from odoo.osv import expression

class DiscussControllerCr(DiscussController):

    @http.route('/mail/inbox/messages', methods=['POST'], type='json', auth='user')
    def discuss_inbox_messages(self, max_id=None, min_id=None, limit=30, **kwargs):
        domain = [('needaction', '=', True)]
        search_domain = []
        if kwargs and 'messageFilter' in kwargs and kwargs.get('messageFilter'):
            domain = expression.AND([domain, kwargs.get('stringifiedDomain')])
            return request.env['mail.message']._message_fetch(
                domain=domain, max_id=max_id, min_id=min_id,
                limit=limit).message_format(), []
        if kwargs and 'stringifiedDomain' in kwargs:
            search_domain = expression.AND([domain, kwargs.get('stringifiedDomain')])
        return request.env['mail.message']._message_fetch(domain=domain, max_id=max_id,
                                                          min_id=min_id, limit=limit).message_format(),request.env['mail.message']._message_fetch(domain=search_domain, max_id=None,
                                                          min_id=None, limit=50).message_format()

    @http.route('/mail/history/messages', methods=['POST'], type='json', auth='user')
    def discuss_history_messages(self, max_id=None, min_id=None, limit=30, **kwargs):
        domain = [('needaction', '=', False)]
        search_domain = []
        if kwargs and 'messageFilter' in kwargs and kwargs.get('messageFilter'):
            domain = expression.AND([domain, kwargs.get('stringifiedDomain')])
            return request.env['mail.message']._message_fetch(
                domain=domain, max_id=max_id, min_id=min_id,
                limit=limit).message_format(), []
        if kwargs and 'stringifiedDomain' in kwargs:
            search_domain = expression.AND([domain, kwargs.get('stringifiedDomain')])
        return request.env['mail.message']._message_fetch(domain=domain, max_id=max_id,
                                                          min_id=min_id, limit=limit).message_format(),request.env['mail.message']._message_fetch(domain=search_domain, max_id=None,
                                                          min_id=None, limit=50).message_format()

    @http.route('/mail/starred/messages', methods=['POST'], type='json', auth='user')
    def discuss_starred_messages(self, max_id=None, min_id=None, limit=30, **kwargs):
        domain = [('starred_partner_ids', 'in', [request.env.user.partner_id.id])]
        search_domain = []
        if kwargs and 'messageFilter' in kwargs and kwargs.get('messageFilter'):
            domain = expression.AND([domain, kwargs.get('stringifiedDomain')])
            return request.env['mail.message']._message_fetch(
                domain=domain, max_id=max_id, min_id=min_id,
                limit=limit).message_format(), []
        if kwargs and 'stringifiedDomain' in kwargs:
            search_domain = expression.AND([domain, kwargs.get('stringifiedDomain')])
        return request.env['mail.message']._message_fetch(
            domain=domain, max_id=max_id, min_id=min_id,
            limit=limit).message_format(),request.env['mail.message']._message_fetch(domain=search_domain, max_id=None,
                                                          min_id=None, limit=50).message_format()
    #
    @http.route('/mail/channel/messages', methods=['POST'], type='json', auth='public')
    def mail_channel_messages(self, channel_id, max_id=None, min_id=None, limit=30, **kwargs):
        channel_member_sudo = request.env['mail.channel.member']._get_as_sudo_from_request_or_raise(request=request,
                                                                                                    channel_id=int(
                                                                                                        channel_id))
        domain = [
            ('res_id', '=', channel_id),
            ('model', '=', 'mail.channel'),
            ('message_type', '!=', 'user_notification'),
        ]
        search_domain = []

        if kwargs and 'stringifiedDomain' in kwargs:
            search_domain = expression.AND([domain, kwargs.get('stringifiedDomain')])
        if kwargs and 'messageFilter' in kwargs and kwargs.get('messageFilter'):
            domain = expression.AND([domain, kwargs.get('stringifiedDomain')])
            messages = channel_member_sudo.env['mail.message']._message_fetch(domain, max_id=max_id, min_id=min_id,
                                                                              limit=limit)
            return messages.message_format(), []
        messages = channel_member_sudo.env['mail.message']._message_fetch(domain, max_id=max_id, min_id=min_id, limit=limit)
        search_messages = channel_member_sudo.env['mail.message']._message_fetch(search_domain, max_id=None, min_id=None, limit=50)
        if not request.env.user._is_public():
            messages.set_message_done()
        return messages.message_format(),search_messages.message_format()

    @http.route('/mail/thread/messages', methods=['POST'], type='json', auth='user')
    def mail_thread_messages(self, thread_model, thread_id, max_id=None, min_id=None, limit=30, **kwargs):
        res = super().mail_thread_messages(thread_model, thread_id, max_id=max_id, min_id=min_id, limit=limit, **kwargs)
        return res,[]
