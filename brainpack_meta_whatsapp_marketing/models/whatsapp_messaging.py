from odoo import models, api, fields, _
from odoo.tools.safe_eval import safe_eval
from odoo import tools
import json
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

MASS_WHATSAPP_BUSINESS_MODELS = ['res.partner', 'whatsapp.messaging.lists']

image_type = ['image/avif', 'image/bmp', 'image/gif', 'image/vnd.microsoft.icon', 'image/jpeg', 'image/png',
              'image/svg+xml', 'image/tiff', 'image/webp']
document_type = ['application/xhtml+xml', 'application/vnd.ms-excel',
                 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/xml',
                 'application/vnd.mozilla.xul+xml', 'application/zip',
                 'application/x-7z-compressed', 'application/x-abiword', 'application/x-freearc',
                 'application/vnd.amazon.ebook', 'application/octet-stream', 'application/x-bzip',
                 'application/x-bzip2', 'application/x-cdf', 'application/x-csh', 'application/msword',
                 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                 'application/vnd.ms-fontobject', 'application/epub+zip', 'application/gzip',
                 'application/java-archive', 'application/json', 'application/ld+json',
                 'application/vnd.apple.installer+xml', 'application/vnd.oasis.opendocument.presentation',
                 'application/vnd.oasis.opendocument.spreadsheet', 'application/vnd.oasis.opendocument.text',
                 'application/ogg', 'application/pdf', 'application/x-httpd-php', 'application/vnd.ms-powerpoint',
                 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/vnd.rar',
                 'application/rtf', 'application/x-sh', 'application/x-tar', 'application/vnd.visio']
audio_type = ['audio/aac', 'audio/midi', 'audio/x-midi', 'audio/mpeg', 'audio/ogg', 'audio/opus', 'audio/wav',
              'audio/webm', 'audio/3gpp', 'audio/3gpp2']
video_type = ['video/x-msvideo', 'video/mp4', 'video/mpeg', 'video/ogg', 'video/mp2t', 'video/webm', 'video/3gpp',
              'video/3gpp2']


class WhatsAppMessaging(models.Model):
    _description = 'Whatsapp Messaging'
    _name = 'whatsapp.messaging'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    def _get_current_model_template(self):
        domain = [('model', 'in', ["res.partner", "whatsapp.messaging.lists"]), ('state', '=', 'added')]

        # Multi Companies and Multi Providers Code Here
        # provider_id = self.env.user.provider_ids.filtered(lambda x: x.company_id == self.env.company)
        # if self.env.user.provider_id:
        if self.env.user:
            provider_id = self.env.user.provider_ids.filtered(lambda x: x.company_id == self.env.company)
            if provider_id:
                provider_id = provider_id[0]
        if provider_id:
            domain.append(('provider_id', '=', provider_id.id))
        else:
            domain.append(('create_uid', '=', self.env.user.id))
        return domain

    name = fields.Char('Name', required='True')

    state = fields.Selection([('draft', 'Draft'), ('in_queue', 'In Queue'), ('sending', 'Sending'), ('done', 'Sent')],
                             string='Status', required=True, copy=False, default='draft',
                             )
    domain = fields.Boolean('Domain')
    partner_ids = fields.Many2many("res.partner")
    whatsapp_messaging_lists_ids = fields.Many2many("whatsapp.messaging.lists")
    wa_messaging_model_id = fields.Many2one('ir.model', string='Recipients Model',
                                            domain=[('model', 'in', MASS_WHATSAPP_BUSINESS_MODELS)], )
    wa_messaging_domain = fields.Char(string='Domain', oldname='domain', default=[])
    body_html = fields.Html('Body', translate=True, sanitize=False)
    schedule_date = fields.Datetime(string='Schedule in the Future')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)

    template_id = fields.Many2one(
        'wa.template', 'Use template', index=True, domain=_get_current_model_template
    )
    attachment_ids = fields.Many2many(
        'ir.attachment', 'whatsapp_messaging_ir_attachments_rel',
        'whatsapp_messaging_id', 'attachment_id', 'Attachments')
    is_partner = fields.Boolean(string='Partner', compute="_compute_partner")
    mail_history_ids = fields.One2many('whatsapp.history', 'whatsapp_messaging_id')
    marketing_contact_mes_history_ids = fields.One2many('marketing.contact.history', 'marketing_contact_id')

    provider_id = fields.Many2one('provider', 'Provider')
    allowed_provider_ids = fields.Many2many('provider', 'Provider', compute='update_allowed_providers')
    received_ratio = fields.Integer(compute="_compute_statistics", string='Received Ratio')
    inqueue_ratio = fields.Integer(compute="_compute_statistics", string='In Queue Ratio')
    sent_ratio = fields.Integer(compute="_compute_statistics", string='Sent Ratio')
    delivered_ratio = fields.Integer(compute="_compute_statistics", string='Delivered Ratio')
    read_ratio = fields.Integer(compute="_compute_statistics", string='Read Ratio')
    fail_ratio = fields.Integer(compute="_compute_statistics", string='Fail Ratio')

    def _compute_statistics(self):

        for rec in self:
            received = len(self.env['whatsapp.history'].search([('type', '=', 'received'), ('whatsapp_messaging_id', '=', rec.id)]).ids)
            inqueue = len(self.env['whatsapp.history'].search([('type', '=', 'in queue'), ('whatsapp_messaging_id', '=', rec.id)]).ids)
            sent = len(self.env['whatsapp.history'].search([('type', '=', 'sent'), ('whatsapp_messaging_id', '=', rec.id)]).ids)
            delivered = len(self.env['whatsapp.history'].search([('type', '=', 'delivered'), ('whatsapp_messaging_id', '=', rec.id)]).ids)
            read = len(self.env['whatsapp.history'].search(
                [('type', '=', 'read'), ('whatsapp_messaging_id', '=', rec.id)]).ids)
            fail = len(self.env['whatsapp.history'].search(
                [('type', '=', 'fail'), ('whatsapp_messaging_id', '=', rec.id)]).ids)

            total_wa_history = len(self.env['whatsapp.history'].search([('whatsapp_messaging_id', '=', rec.id)]).ids)
            if total_wa_history != 0:
                rec.received_ratio = (received / total_wa_history) * 100
                rec.inqueue_ratio = (inqueue / total_wa_history) * 100
                rec.sent_ratio = (sent / total_wa_history) * 100
                rec.delivered_ratio = (delivered / total_wa_history) * 100
                rec.read_ratio = (read / total_wa_history) * 100
                rec.fail_ratio = (fail / total_wa_history) * 100
            else:
                rec.received_ratio = 0
                rec.inqueue_ratio = 0
                rec.sent_ratio = 0
                rec.delivered_ratio = 0
                rec.read_ratio = 0
                rec.fail_ratio = 0

    def _action_view_documents_filtered(self, view_filter):
        action = self.env["ir.actions.actions"]._for_xml_id("brainpack_meta_whatsapp.whatsapp_history_action")
        action['domain'] = [('type', '=', view_filter), ('whatsapp_messaging_id', '=', self.id)]
        if view_filter == 'read':
            action['name'] = 'Read'
            action['display_name'] = 'Read'
        if view_filter == 'in queue':
            action['name'] = 'In Queue'
            action['display_name'] = 'In Queue'
        if view_filter == 'sent':
            action['name'] = 'Sent'
            action['display_name'] = 'Sent'
        if view_filter == 'delivered':
            action['name'] = 'Delivered'
            action['display_name'] = 'Delivered'
        if view_filter == 'received':
            action['name'] = 'Received'
            action['display_name'] = 'Received'
        if view_filter == 'fail':
            action['name'] = 'Fail'
            action['display_name'] = 'Fail'
        return action

    def action_view_inqueue(self):
        return self._action_view_documents_filtered('in queue')

    def action_view_sent(self):
        return self._action_view_documents_filtered('sent')

    def action_view_delivered(self):
        return self._action_view_documents_filtered('delivered')

    def action_view_received(self):
        return self._action_view_documents_filtered('received')

    def action_view_read(self):
        return self._action_view_documents_filtered('read')

    def action_view_fail(self):
        return self._action_view_documents_filtered('fail')

    @api.depends('company_id')
    def update_allowed_providers(self):
        self.allowed_provider_ids = self.env.user.provider_ids

    @api.onchange('company_id', 'provider_id')
    def onchange_company_provider(self):
        self.template_id = False
        return {'domain': {
            'template_id': [('model_id.model', '=', 'res.partner'), ('provider_id', '=', self.provider_id.id)]}}

    @api.depends('wa_messaging_model_id')
    def _compute_partner(self):
        # simple logic, but you can do much more here
        for rec in self:
            if rec.wa_messaging_model_id.model == 'res.partner':
                rec.is_partner = True
            else:
                rec.is_partner = False

    def action_schedule_date(self):
        self.ensure_one()
        action = self.env.ref('brainpack_meta_whatsapp_marketing.whatsapp_messaging_schedule_date_action').read()[0]
        action['context'] = dict(self.env.context, default_whatsapp_messaging_id=self.id)
        return action

    def put_in_queue(self):
        self.write({'state': 'in_queue'})

    def cancel_mass_mailing(self):
        self.write({'state': 'draft', 'schedule_date': False})

    @api.onchange('template_id')
    def onchange_template_id_wrapper(self):
        self.ensure_one()
        active_model = str('res.partner')
        for record in self:
            if record.template_id:
                user_error = False
                if record.template_id and record.template_id.components_ids and record.wa_messaging_model_id and record.wa_messaging_model_id.model == 'whatsapp.messaging.lists':
                    for component in record.template_id.components_ids:
                        if component.variables_ids:
                            user_error = True
                            break
                if user_error:
                    raise UserError(
                        ("You can not select this template. please select another one!"))
                record.body_html = \
                record.template_id._render_field('body_html', [self.env.user.partner_id.id], compute_lang=True)[
                    self.env.user.partner_id.id]
            else:
                record.body_html = ''

    def remaining_contacts(self, contacts):
        whatsapp_numbers = self.env['whatsapp.history'].search(
            [('whatsapp_messaging_id', '=', self.id), ('type', '=', 'sent')]).mapped('phone')
        contacts_ids = [x.id for x in contacts if x.phone not in whatsapp_numbers]
        return self.env['whatsapp.messaging.lists.contacts'].browse(contacts_ids)

    def remaining_partners(self, partners):
        res_ids = self.env['mail.message'].search(
            [('whatsapp_messaging_id', '=', self.id), ('message_type', '=', 'comment')]).mapped('res_id')
        ramaning_partner_ids = [x for x in partners.ids if x not in res_ids]
        return self.env['res.partner'].browse(ramaning_partner_ids)

    @api.model
    def _process_whatsapp_messaging_queue(self):
        whatsapp_messagings = self.search(
            [('state', 'in', ('in_queue', 'sending')), '|', ('schedule_date', '<', fields.Datetime.now()),
             ('schedule_date', '=', False)])
        for whatsapp_messaging in whatsapp_messagings:
            # Multi Companies and Multi Providers Code Here, We have passed Default Provider for Scheduled Actions
            # provider_id = whatsapp_messaging.user_id.provider_ids.filtered(lambda x: x.company_id == self.env.company and x.chat_api_authenticated)
            provider_id = whatsapp_messaging.provider_id
            user = whatsapp_messaging.user_id
            # mass_mailing = mass_mailing.with_context(**user.sudo(user=user).context_get())
            # if len(mass_mailing.get_remaining_recipients()) > 0:
            #     mass_mailing.state = 'sending'
            #     mass_mailing.send_mail()
            # else:
            #     mass_mailing.write({'state': 'done', 'sent_date': fields.Datetime.now()})
            #
            if whatsapp_messaging.is_partner:
                partners = False
                if whatsapp_messaging.wa_messaging_domain and whatsapp_messaging.domain:
                    domain = safe_eval(whatsapp_messaging.wa_messaging_domain)
                    partners = self.env['res.partner'].search(domain)
                else:
                    partners = whatsapp_messaging.partner_ids

                if partners:
                    partners = whatsapp_messaging.remaining_partners(partners)
                    for partner in partners:
                        whatsapp_messaging.write({'state': 'sending'})
                        if partner.mobile:
                            whatsapp_messaging.write({'marketing_contact_mes_history_ids': [
                                            (0, 0, {'phone': partner.mobile})]})

                            _logger.info("partner Mobile (Whatsapp Number) %s", partner.mobile)
                            flag = True
                            if provider_id.provider == 'chat_api':
                                flag = False
                                answer = provider_id.check_phone(partner.mobile.strip('+').replace(" ", ""))
                                if answer.status_code == 200:
                                    dict_val = json.loads(answer.text)
                                    _logger.info("partner Mobile (Whatsapp Number) %s", dict_val.get('result'))
                                    if 'result' in dict_val:
                                        if dict_val['result'] == 'exists':
                                            flag = True
                            if flag:
                                partner.write({'mobile': partner.mobile.strip('+').replace(' ', '')})
                                user_partner = user.partner_id
                                # users = request.env['res.users'].sudo().search([])
                                part_lst = []
                                part_lst.append(partner.id)
                                part_lst.append(user_partner.id)
                                # Multi Companies and Multi Providers Code Here
                                # provider_channel_id = partner.channel_provider_line_ids.filtered(
                                #     lambda s: s.provider_id == whatsapp_messaging.user_id.provider_id)
                                provider_channel_id = partner.channel_provider_line_ids.filtered(
                                    lambda s: s.provider_id == provider_id)
                                if provider_channel_id:
                                    channel = provider_channel_id.channel_id
                                    if user_partner.id not in channel.channel_partner_ids.ids and whatsapp_messaging.user_id.has_group(
                                            'base.group_user') and whatsapp_messaging.user_id.has_group(
                                        'brainpack_meta_whatsapp.whatsapp_group_user'):
                                        channel.sudo().write({'channel_partner_ids': [(4, user_partner.id)]})
                                else:
                                    name = partner.mobile
                                    channel = self.env['mail.channel'].create({
                                        #'public': 'public',
                                        'channel_type': 'chat',
                                        'name': name,
                                        'whatsapp_channel': True,
                                        'channel_partner_ids': [(4, partner.id)],
                                    })
                                    channel.write({'channel_member_ids': [(5, 0, 0)] + [
                                        (0, 0, {'partner_id': line_vals}) for line_vals in part_lst]})
                                    # self.partner_id.write({'channel_id': channel.id})
                                    # Multi Companies and Multi Providers Code Here
                                    # partner.write({'channel_provider_line_ids': [
                                    #     (0, 0, {'channel_id': channel.id, 'provider_id': whatsapp_messaging.user_id.provider_id.id})]})
                                    partner.write({'channel_provider_line_ids': [
                                        (0, 0, {'channel_id': channel.id, 'provider_id': provider_id.id})]})
                                if channel:
                                    if whatsapp_messaging.template_id:
                                        wa_message_values = {}
                                        if whatsapp_messaging.body_html != '':
                                            wa_message_values.update({'body':
                                                                          whatsapp_messaging.template_id._render_field(
                                                                              'body_html', [partner.id],
                                                                              compute_lang=True)[partner.id]})
                                        if whatsapp_messaging.attachment_ids:
                                            wa_message_values.update(
                                                {'attachment_ids': [(4, attac_id.id) for attac_id in
                                                                    whatsapp_messaging.attachment_ids]})
                                        wa_message_values.update({
                                            'author_id': user_partner.id,
                                            'email_from': user_partner.email or '',
                                            'model': 'mail.channel',
                                            'message_type': 'wa_msgs',
                                            'isWaMsgs': True,
                                            'subtype_id': self.env['ir.model.data'].sudo()._xmlid_to_res_id(
                                                'mail.mt_comment'),
                                            # 'channel_ids': [(4, channel.id)],
                                            'partner_ids': [(4, user_partner.id)],
                                            'res_id': channel.id,
                                            'reply_to': user_partner.email,
                                            'whatsapp_messaging_id': whatsapp_messaging.id,
                                        })
                                        wa_attach_message = self.env['mail.message'].sudo().with_context(
                                            {'template_send': True, 'wa_template': whatsapp_messaging.template_id,
                                             'active_model_id': partner.id, 'active_model': self._name,
                                             'attachment_ids': whatsapp_messaging.attachment_ids.ids, 'user_id': user,
                                             'cron': True}).create(
                                            wa_message_values)
                                        notifications = channel._channel_message_notifications(wa_attach_message)
                                        self.env['bus.bus']._sendmany(notifications)

                                        message_values = {
                                            'body':
                                                whatsapp_messaging.template_id._render_field('body_html', [partner.id],
                                                                                             compute_lang=True)[
                                                    partner.id],
                                            'author_id': user_partner.id,
                                            'email_from': user_partner.email or '',
                                            'model': 'res.partner',
                                            'message_type': 'comment',
                                            'isWaMsgs': True,
                                            'subtype_id': self.env['ir.model.data'].sudo()._xmlid_to_res_id(
                                                'mail.mt_comment'),
                                            # 'channel_ids': [(4, channel.id)],
                                            'partner_ids': [(4, user_partner.id)],
                                            'res_id': partner.id,
                                            'reply_to': user_partner.email,
                                            'attachment_ids': [(4, attac_id.id) for attac_id in self.attachment_ids],
                                            'whatsapp_messaging_id': whatsapp_messaging.id,
                                        }
                                        if whatsapp_messaging.attachment_ids:
                                            message_values.update({})
                                        message = self.env['mail.message'].sudo().create(
                                            message_values)
                                        wa_attach_message.chatter_wa_model = 'res.partner'
                                        wa_attach_message.chatter_wa_res_id = partner.id
                                        wa_attach_message.chatter_wa_message_id = message.id
                                        notifications = channel._channel_message_notifications(message)
                                        self.env['bus.bus']._sendmany(notifications)
                                    else:
                                        if tools.html2plaintext(whatsapp_messaging.body_html) != '':
                                            message_values = {
                                                'body': tools.html2plaintext(whatsapp_messaging.body_html),
                                                'author_id': user_partner.id,
                                                'email_from': user_partner.email or '',
                                                'model': 'mail.channel',
                                                'message_type': 'wa_msgs',
                                                'isWaMsgs': True,
                                                'subtype_id': self.env['ir.model.data'].sudo()._xmlid_to_res_id(
                                                    'mail.mt_comment'),
                                                # 'channel_ids': [(4, channel.id)],
                                                'partner_ids': [(4, user_partner.id)],
                                                'res_id': channel.id,
                                                'reply_to': user_partner.email,
                                                'whatsapp_messaging_id': whatsapp_messaging.id,
                                            }
                                            if whatsapp_messaging.template_id:
                                                wa_message_body = self.env['mail.message'].sudo().with_context(
                                                    {'template_send': True,
                                                     'wa_template': whatsapp_messaging.template_id,
                                                     'active_model_id': partner.id, 'active_model': self._name,
                                                     'user_id': user, 'cron': True}).create(message_values)
                                            else:
                                                wa_message_body = self.env['mail.message'].sudo().with_context(
                                                    {'cron': True, 'user_id': user}).create(
                                                    message_values)
                                            notifications = channel._channel_message_notifications(wa_message_body)
                                            self.env['bus.bus']._sendmany(notifications)

                                            message_values = {
                                                'body': whatsapp_messaging.body_html,
                                                'author_id': user_partner.id,
                                                'email_from': user_partner.email or '',
                                                'model': 'res.partner',
                                                'message_type': 'comment',
                                                'isWaMsgs': True,
                                                'subtype_id': self.env['ir.model.data'].sudo()._xmlid_to_res_id(
                                                    'mail.mt_comment'),
                                                # 'channel_ids': [(4, channel.id)],
                                                'partner_ids': [(4, user_partner.id)],
                                                'res_id': partner.id,
                                                'reply_to': user_partner.email,
                                                'whatsapp_messaging_id': whatsapp_messaging.id,
                                            }
                                            message = self.env['mail.message'].sudo().create(
                                                message_values)
                                            wa_message_body.chatter_wa_model = 'res.partner'
                                            wa_message_body.chatter_wa_res_id = partner.id
                                            wa_message_body.chatter_wa_message_id = message.id
                                            notifications = channel._channel_message_notifications(message)
                                            self.env['bus.bus']._sendmany(notifications)

                                        if whatsapp_messaging.attachment_ids:
                                            message_values = {
                                                'body': "",
                                                'author_id': user_partner.id,
                                                'email_from': user_partner.email or '',
                                                'model': 'mail.channel',
                                                'message_type': 'wa_msgs',
                                                'isWaMsgs': True,
                                                'subtype_id': self.env['ir.model.data'].sudo()._xmlid_to_res_id(
                                                    'mail.mt_comment'),
                                                # 'channel_ids': [(4, channel.id)],
                                                'partner_ids': [(4, user_partner.id)],
                                                'res_id': channel.id,
                                                'reply_to': user_partner.email,
                                                'attachment_ids': [(4, attac_id.id) for attac_id in
                                                                   whatsapp_messaging.attachment_ids],
                                                'whatsapp_messaging_id': whatsapp_messaging.id,
                                            }
                                            if whatsapp_messaging.template_id:
                                                wa_attach_message = self.env['mail.message'].sudo().with_context(
                                                    {'template_send': True,
                                                     'wa_template': whatsapp_messaging.template_id,
                                                     'active_model_id': partner.id, 'active_model': self._name,
                                                     'attachment_ids': whatsapp_messaging.attachment_ids.ids,
                                                     'user_id': user, 'cron': True}).create(
                                                    message_values)
                                            else:
                                                wa_attach_message = self.env['mail.message'].sudo().with_context(
                                                    {'cron': True, 'user_id': user}).create(
                                                    message_values)
                                            # wa_attach_message = self.env['mail.message'].sudo().create(
                                            #     message_values)
                                            notifications = channel._channel_message_notifications(wa_attach_message)
                                            self.env['bus.bus']._sendmany(notifications)

                                            message_values = {
                                                'author_id': user_partner.id,
                                                'email_from': user_partner.email or '',
                                                'model': 'res.partner',
                                                'message_type': 'comment',
                                                'isWaMsgs': True,
                                                'subtype_id': self.env['ir.model.data'].sudo()._xmlid_to_res_id(
                                                    'mail.mt_comment'),
                                                # 'channel_ids': [(4, channel.id)],
                                                'partner_ids': [(4, user_partner.id)],
                                                'res_id': partner.id,
                                                'reply_to': user_partner.email,
                                                'attachment_ids': [(4, attac_id.id) for attac_id in
                                                                   whatsapp_messaging.attachment_ids],
                                                'whatsapp_messaging_id': whatsapp_messaging.id,
                                            }
                                            if whatsapp_messaging.attachment_ids:
                                                message_values.update({})
                                            message = self.env['mail.message'].sudo().create(
                                                message_values)
                                            wa_attach_message.chatter_wa_model = 'res.partner'
                                            wa_attach_message.chatter_wa_res_id = partner.id
                                            wa_attach_message.chatter_wa_message_id = message.id
                                            notifications = channel._channel_message_notifications(message)
                                            self.env['bus.bus']._sendmany(notifications)
                                self._cr.commit()
                                # message_values = {
                                #     'body': tools.html2plaintext(whatsapp_messaging.body_html) or '',
                                #     'author_id': user_partner.id,
                                #     'email_from': user_partner.email or '',
                                #     'model': 'mail.channel',
                                #     'message_type': 'wa_msgs',
                                #     'isWaMsgs': True,
                                #     'subtype_id': self.env['ir.model.data'].sudo().xmlid_to_res_id('mail.mt_comment'),
                                #     'channel_ids': [(4, channel.id)],
                                #     'partner_ids': [(4, user_partner.id)],
                                #     'res_id': channel.id,
                                #     'reply_to': user_partner.email,
                                # }
                                # message = self.env['mail.message'].sudo().with_context({'company_id': whatsapp_messaging.company_id.id}).create(
                                #     message_values)
                                # channel._notify_thread(message)
            else:
                for whatsapp_messaging_lists_id in whatsapp_messaging.whatsapp_messaging_lists_ids:
                    contacts = whatsapp_messaging.remaining_contacts(whatsapp_messaging_lists_id.contacts_ids)
                    for contact in contacts:
                        if contact.phone:
                            _logger.info("contact Mobile (Whatsapp Number) %s", contact.phone)

                            print(">>>>>>>>>>>>>>>..................", contact.phone, whatsapp_messaging)
                            whatsapp_messaging.write({'marketing_contact_mes_history_ids': [
                                (0, 0, {'phone': contact.phone})]})

                            flag = True
                            if provider_id.provider == 'chat_api':
                                flag = False
                                answer = provider_id.check_phone(contact.phone.strip('+').replace(" ", ""))
                                if answer.status_code == 200:
                                    dict_val = json.loads(answer.text)
                                    _logger.info("contact Mobile (Whatsapp Number) %s", dict_val.get('result'))
                                    if 'result' in dict_val:
                                        if dict_val['result'] == 'exists':
                                            flag = True
                            if flag:
                                if whatsapp_messaging.template_id:
                                    params = []
                                    for component in whatsapp_messaging.template_id.components_ids:
                                        template_dict = {}

                                        if component.type in ['body', 'footer']:
                                            if component.variables_ids:
                                                template_dict.update({'type': component.type})
                                                parameters = []
                                                template_dict.update({'parameters': parameters})

                                        if component.type == 'header':
                                            if component.formate == 'text':
                                                if component.variables_ids:
                                                    template_dict.update({'type': component.type})
                                                    parameters = []
                                                    template_dict.update({'parameters': parameters})
                                            if component.formate == 'media':
                                                IrConfigParam = self.env['ir.config_parameter'].sudo()
                                                base_url = IrConfigParam.get_param('web.base.url', False)

                                                if component.media_type == 'document':
                                                    if whatsapp_messaging.attachment_ids:
                                                        template_dict.update({'type': component.type})
                                                        parameters = [
                                                            {'type': component.media_type, 'document': {
                                                                "link": base_url + "/web/content/" + str(
                                                                    whatsapp_messaging.attachment_ids.ids[0]),
                                                                "filename": self.env[
                                                                    'ir.attachment'].sudo().browse(
                                                                    whatsapp_messaging.attachment_ids.ids[
                                                                        0]).name}}]
                                                        template_dict.update({'parameters': parameters})
                                                if component.media_type == 'video':
                                                    if self.env.context.get('attachment_ids'):
                                                        template_dict.update({'type': component.type})
                                                        parameters = [{'type': component.media_type, 'video': {
                                                            "link": base_url + "/web/content/" + str(
                                                                whatsapp_messaging.attachment_ids.ids[0]),
                                                            "filename": self.env['ir.attachment'].sudo().browse(
                                                                whatsapp_messaging.attachment_ids.ids[
                                                                    0]).name}}]
                                                        template_dict.update({'parameters': parameters})
                                                if component.media_type == 'image':
                                                    template_dict.update({'type': component.type})
                                                    parameters = [{'type': component.media_type, 'image': {
                                                        "link": base_url + "/web/image/ir.attachment/" + str(
                                                            whatsapp_messaging.attachment_ids.ids[
                                                                0]) + "/datas",
                                                    }}]
                                                    template_dict.update({'parameters': parameters})

                                        if bool(template_dict):
                                            params.append(template_dict)

                                    if provider_id.provider == 'chat_api':
                                        answer = provider_id.direct_send_template(
                                            whatsapp_messaging.template_id.name,
                                            whatsapp_messaging.template_id.lang.iso_code,
                                            whatsapp_messaging.template_id.namespace, contact.phone, params)
                                        if answer.status_code == 200:
                                            dict = json.loads(answer.text)
                                            if 'sent' in dict and dict.get('sent'):
                                                vals = {
                                                    'provider_id': provider_id.id,
                                                    'author_id': user.partner_id.id,
                                                    'message': tools.html2plaintext(
                                                        whatsapp_messaging.body_html),
                                                    'type': 'in queue',
                                                    'message_id': dict['id'],
                                                    'phone': contact.phone,
                                                    'whatsapp_messaging_id': whatsapp_messaging.id,
                                                }
                                                self.env['whatsapp.history'].sudo().create(vals)

                                    if provider_id.provider == 'graph_api':
                                        answer = provider_id.direct_send_template(
                                            whatsapp_messaging.template_id.name,
                                            whatsapp_messaging.template_id.lang.iso_code,
                                            whatsapp_messaging.template_id.namespace, contact, params)
                                        if answer.status_code == 200:
                                            dict = json.loads(answer.text)
                                            if 'messages' in dict and dict.get('messages') and dict.get('messages')[
                                                0].get('id'):
                                                vals = {
                                                    'provider_id': provider_id.id,
                                                    'author_id': user.partner_id.id,
                                                    'message': tools.html2plaintext(
                                                        whatsapp_messaging.body_html),
                                                    'type': 'in queue',
                                                    'message_id': dict.get('messages')[0].get('id'),
                                                    'phone': contact.phone,
                                                    'whatsapp_messaging_id': whatsapp_messaging.id,
                                                    'model': self._name,
                                                }
                                                self.env['whatsapp.history'].sudo().create(vals)

                                else:
                                    if tools.html2plaintext(whatsapp_messaging.body_html) != '':

                                        if provider_id.provider == 'chat_api':
                                            answer = provider_id.direct_send_message(contact.phone,
                                                                                     tools.html2plaintext(
                                                                                         whatsapp_messaging.body_html))
                                            if answer.status_code == 200:
                                                dict = json.loads(answer.text)

                                                if 'sent' in dict and dict.get('sent'):
                                                    vals = {
                                                        'provider_id': provider_id.id,
                                                        'author_id': user.partner_id.id,
                                                        'message': tools.html2plaintext(
                                                            whatsapp_messaging.body_html),
                                                        'type': 'in queue',
                                                        'message_id': dict['id'],
                                                        'phone': contact.phone,
                                                        'whatsapp_messaging_id': whatsapp_messaging.id,
                                                    }
                                                    self.env['whatsapp.history'].sudo().create(vals)
                                        if provider_id.provider == 'graph_api':
                                            answer = provider_id.direct_send_message(contact,
                                                                                     tools.html2plaintext(
                                                                                         whatsapp_messaging.body_html))
                                            if answer.status_code == 200:
                                                dict = json.loads(answer.text)

                                                if 'messages' in dict and dict.get('messages') and dict.get('messages')[
                                                    0].get('id'):
                                                    vals = {
                                                        'provider_id': provider_id.id,
                                                        'author_id': user.partner_id.id,
                                                        'message': tools.html2plaintext(
                                                            whatsapp_messaging.body_html),
                                                        'type': 'in queue',
                                                        'message_id': dict.get('messages')[0].get('id'),
                                                        'phone': contact.phone,
                                                        'whatsapp_messaging_id': whatsapp_messaging.id,
                                                        'model': self._name,
                                                    }
                                                    self.env['whatsapp.history'].sudo().create(vals)

                                    if whatsapp_messaging.attachment_ids:
                                        for attachment in whatsapp_messaging.attachment_ids:
                                            if provider_id.provider == 'chat_api':
                                                answer = provider_id.direct_send_file(contact.phone,
                                                                                      attachment)
                                                if answer.status_code == 200:
                                                    dict = json.loads(answer.text)
                                                    if 'sent' in dict and dict.get('sent'):
                                                        vals = {
                                                            'provider_id': provider_id.id,
                                                            'author_id': user.partner_id.id,
                                                            'attachment_ids': [(4, attachment.id)],
                                                            'type': 'in queue',
                                                            'message_id': dict['id'],
                                                            'phone': contact.phone,
                                                            'whatsapp_messaging_id': whatsapp_messaging.id,
                                                        }
                                                        self.env['whatsapp.history'].sudo().create(vals)

                                            if provider_id.provider == 'graph_api':
                                                sent_type = False
                                                if attachment.mimetype in image_type:
                                                    sent_type = 'image'
                                                elif attachment.mimetype in document_type:
                                                    sent_type = 'document'
                                                elif attachment.mimetype in audio_type:
                                                    sent_type = 'audio'
                                                elif attachment.mimetype in video_type:
                                                    sent_type = 'video'
                                                else:
                                                    sent_type = 'image'

                                                answer = provider_id.send_image(contact, attachment)
                                                if answer.status_code == 200:
                                                    dict = json.loads(answer.text)
                                                    media_id = dict.get('id')
                                                    getimagebyid = provider_id.direct_get_image_by_id(media_id,
                                                                                               contact,
                                                                                               sent_type,
                                                                                               attachment)
                                                    if getimagebyid.status_code == 200:
                                                        imagedict = json.loads(getimagebyid.text)
                                                        if 'messages' in imagedict and imagedict.get('messages'):
                                                            vals = {
                                                                'provider_id': provider_id.id,
                                                                'author_id': user.partner_id.id,
                                                                'attachment_ids': [(4, attachment.id)],
                                                                'type': 'in queue',
                                                                'message_id': imagedict.get('id'),
                                                                'phone': contact.phone,
                                                                'whatsapp_messaging_id': whatsapp_messaging.id,
                                                                'model': self._name,
                                                            }
                                                            self.env['whatsapp.history'].sudo().create(vals)

                                            # else:
                                            #     res.write({'type': 'fail'})
                                            #     if 'error' in dict:
                                            #         res.write({'fail_reason': dict.get('error').get('message')})
                                            # else:
                                            #     if 'message' in dict:
                                            #         raise UserError(
                                            #             (dict.get('message')))
                                            #     if 'error' in dict:
                                            #         raise UserError(
                                            #             (dict.get('error').get('message')))
                            self._cr.commit()

            whatsapp_messaging.write({'state': 'done'})
