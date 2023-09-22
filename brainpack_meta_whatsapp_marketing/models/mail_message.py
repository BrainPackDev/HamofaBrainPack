import logging
import re

from odoo import _, api, fields, models, modules, tools
from odoo.http import request
from binascii import Error as binascii_error
from collections import defaultdict
from odoo.exceptions import AccessError, UserError, ValidationError
from operator import itemgetter
from odoo.tools.misc import clean_context

_logger = logging.getLogger(__name__)
_image_dataurl = re.compile(r'(data:image/[a-z]+?);base64,([a-z0-9+/\n]{3,}=*)\n*([\'"])(?: data-filename="([^"]*)")?', re.I)

class Message(models.Model):
    """ Messages model: system notification (replacing res.log notifications),
        comments (OpenChatter discussion) and incoming emails. """
    _inherit = 'mail.message'

    whatsapp_messaging_id = fields.Many2one('whatsapp.messaging')

    @api.model_create_multi
    def create(self, values_list):
        # Multi Companies and Multi Providers Code Here
        #provider_id = self.env.user.provider_ids.filtered(lambda x: x.company_id == self.env.company)[0]
        provider_id = False
        # if self._context.get('provider_id'):
        #     provider_id = self._context.get('provider_id')

        tracking_values_list = []
        for values in values_list:
            if 'email_from' not in values:  # needed to compute reply_to
                _author_id, email_from = self.env['mail.thread']._message_compute_author(values.get('author_id'),
                                                                                         email_from=None,
                                                                                         raise_on_email=False)
                values['email_from'] = email_from
            if not values.get('message_id'):
                values['message_id'] = self._get_message_id(values)
            if 'reply_to' not in values:
                values['reply_to'] = self._get_reply_to(values)
            if 'record_name' not in values and 'default_record_name' not in self.env.context:
                values['record_name'] = self._get_record_name(values)

            if 'attachment_ids' not in values:
                values['attachment_ids'] = []
            # extract base64 images
            if 'body' in values:
                Attachments = self.env['ir.attachment'].with_context(clean_context(self._context))
                data_to_url = {}

                def base64_to_boundary(match):
                    key = match.group(2)
                    if not data_to_url.get(key):
                        name = match.group(4) if match.group(4) else 'image%s' % len(data_to_url)
                        try:
                            attachment = Attachments.create({
                                'name': name,
                                'datas': match.group(2),
                                'res_model': values.get('model'),
                                'res_id': values.get('res_id'),
                            })
                        except binascii_error:
                            _logger.warning(
                                "Impossible to create an attachment out of badly formated base64 embedded image. Image has been removed.")
                            return match.group(
                                3)  # group(3) is the url ending single/double quote matched by the regexp
                        else:
                            attachment.generate_access_token()
                            values['attachment_ids'].append((4, attachment.id))
                            data_to_url[key] = [
                                '/web/image/%s?access_token=%s' % (attachment.id, attachment.access_token), name]
                    return '%s%s alt="%s"' % (data_to_url[key][0], match.group(3), data_to_url[key][1])

                values['body'] = _image_dataurl.sub(base64_to_boundary, tools.ustr(values['body']))

            # delegate creation of tracking after the create as sudo to avoid access rights issues
            tracking_values_list.append(values.pop('tracking_value_ids', False))

        messages = super(Message, self.with_context({'whatsapp_marketing':True})).create(values_list)

        check_attachment_access = []
        if all(isinstance(command, int) or command[0] in (4, 6) for values in values_list for command in
               values.get('attachment_ids')):
            for values in values_list:
                for command in values.get('attachment_ids'):
                    if isinstance(command, int):
                        check_attachment_access += [command]
                    elif command[0] == 6:
                        check_attachment_access += command[2]
                    else:  # command[0] == 4:
                        check_attachment_access += [command[1]]
        else:
            check_attachment_access = messages.mapped('attachment_ids').ids  # fallback on read if any unknow command
        if check_attachment_access:
            self.env['ir.attachment'].browse(check_attachment_access).check(mode='read')

        for message, values, tracking_values_cmd in zip(messages, values_list, tracking_values_list):
            if tracking_values_cmd:
                vals_lst = [dict(cmd[2], mail_message_id=message.id) for cmd in tracking_values_cmd if
                            len(cmd) == 3 and cmd[0] == 0]
                other_cmd = [cmd for cmd in tracking_values_cmd if len(cmd) != 3 or cmd[0] != 0]
                if vals_lst:
                    self.env['mail.tracking.value'].sudo().create(vals_lst)
                if other_cmd:
                    message.sudo().write({'tracking_value_ids': tracking_values_cmd})

            if message.is_thread_message(values):
                message._invalidate_documents(values.get('model'), values.get('res_id'))

        for values in values_list:
            if values.get('message_type') == 'wa_msgs':
                vals = {}
                user = self.env.user
                if user.id != self.env.ref('base.public_user').id:
                    if 'user_id' in self.env.context and self.env.context.get('user_id'):
                        user = self.env.context.get('user_id')
                    if values.get('model') == 'mail.channel':
                        channel_company_line_id = self.env['channel.provider.line'].search(
                            [('channel_id', '=', message.res_id)])
                        # phone change to mobile
                        if channel_company_line_id.partner_id.mobile:
                            phone_no = channel_company_line_id.partner_id.mobile.strip('+').replace(' ', '')
                        if channel_company_line_id.provider_id:
                            provider_id = channel_company_line_id.provider_id

                        # Multi Companies and Multi Providers Code Here
                        # provider_id = False
                        if provider_id:
                                vals = {
                                    'provider_id': provider_id[0].id,
                                    'author_id': user.partner_id.id,
                                    'message': values.get('body').replace('<br/>', '\n'),
                                    'type': 'in queue',
                                    'partner_id': channel_company_line_id.partner_id.id,
                                    'phone': channel_company_line_id.partner_id.mobile,
                                    'attachment_ids': values.get('attachment_ids'),
                                    'model': self._context.get('active_model','mail.channel'),
                                }
                                if 'whatsapp_messaging_id' in values:
                                    vals.update({'whatsapp_messaging_id':values.get('whatsapp_messaging_id')})

                                # if 'user_id' in self.env.context and self.env.context.get('user_id'):
                                #     vals.update({'provider_id': self.env.context.get('user_id').provider_id.id})
                        else:
                            raise AccessError(_("Please add provider in User!"))

                    else:
                        partner = False
                        data = self.env[values.get('model')].sudo().search_read(
                            [('id', '=', int(values.get('res_id')))])
                        if values.get('model') == 'res.partner':
                            partner = self.env['res.partner'].browse(data[0]['id'])
                        elif 'partner_id' in data[0]:
                            if data[0]['partner_id']:
                                partner = self.env['res.partner'].browse(data[0]['partner_id'][0])
                            else:
                                raise AccessError(_("Partner must be Required for whatsapp message!"))
                        else:
                            raise AccessError(_("Partner must be Required for whatsapp message!"))

                        if partner and partner.mobile:

                            # if provider_id:
                            #     provider_channel_id = partner.channel_provider_line_ids.filtered(
                            #         lambda s: s.provider_id == provider_id)
                            provider_id = user.provider_id
                            if provider_id:
                                provider_channel_id = partner.channel_provider_line_ids.filtered(
                                    lambda s: s.provider_id == provider_id)
                            else:
                                raise AccessError(_("Please add provider in User!"))
                            user_partner = user.partner_id
                            part_lst = [partner.id, user_partner.id]

                            if provider_channel_id:
                                channel = provider_channel_id.channel_id

                                if user_partner.id not in channel.channel_partner_ids.ids:
                                    channel.sudo().write({'channel_partner_ids': [(4, user_partner.id)]})
                            else:
                                name = partner.mobile
                                channel = self.env['mail.channel'].create({
                                    #'public': 'public',
                                    'channel_type': 'chat',
                                    'email_send': False,
                                    'name': name,
                                    'whatsapp_channel': True,
                                    'channel_partner_ids': part_lst,
                                })
                                channel.write({'channel_member_ids': [(5, 0, 0)] + [
                                    (0, 0, {'partner_id': line_vals}) for line_vals in part_lst]})
                                # self.partner_id.write({'channel_id': channel.id})
                                if provider_id and user.id == self.env.ref('base.public_user').id:
                                    partner.write({'channel_provider_line_ids': [
                                        (0, 0, {'channel_id': channel.id, 'provider_id': provider_id.id})]})
                                else:
                                    raise AccessError(_("Please add provider in User!"))

                            message_values = {
                                'body': values.get('body'),
                                'author_id': user_partner.id,
                                'email_from': user_partner.email or '',
                                'model': values.get('model'),
                                'message_type': 'comment',
                                'isWaMsgs': True,
                                'subtype_id': self.env['ir.model.data'].sudo()._xmlid_to_res_id('mail.mt_comment'),
                                # 'channel_ids': [(4, channel.id)],
                                'partner_ids': [(4, user_partner.id)],
                                'res_id': values.get('res_id'),
                                'reply_to': user_partner.email,
                            }

                            if values.get('attachment_ids'):
                                message_values.update({'attachment_ids': values.get('attachment_ids')})
                            # message_comment = self.env['mail.message'].sudo().with_context({'provider_id': self.provider_id}).create(
                            #     message_values)
                            message_comment = self.env['mail.message'].sudo().create(
                                message_values)
                            notifications = channel._channel_message_notifications(message_comment)
                            self.env['bus.bus']._sendmany(notifications)
                            # phone change to mobile
                            phone_no = partner.mobile.strip('+').replace(' ', '')
                            if provider_id:
                                # phone change to mobile
                                vals = {
                                    'provider_id': provider_id.id,
                                    'author_id': user.partner_id.id,
                                    'message': values.get('body'),
                                    'type': 'in queue',
                                    'partner_id': partner.id,
                                    'phone': partner.mobile,
                                    'attachment_ids': values.get('attachment_ids'),
                                    'model': self._context.get('active_model','mail.channel'),
                                }

                                if 'whatsapp_messaging_id' in values:
                                    vals.update({'whatsapp_messaging_id': values.get('whatsapp_messaging_id')})
                                # if 'user_id' in self.env.context and  self.env.context.get('user_id'):
                                #     vals.update({'provider_id':self.env.context.get('user_id').provider_id.id})
                            else:
                                raise AccessError(_("Please add provider in User!"))

                            for mes in messages:
                                mes.model = 'mail.channel'
                                mes.res_id = channel.id
                                mes.chatter_wa_model = values.get('model'),
                                mes.chatter_wa_res_id = values.get('res_id')
                                mes.chatter_wa_message_id = message_comment.id
                                mes.chatter_wa_model = mes.chatter_wa_model.split("'")[1]
                                # mes.channel_ids = [(4,channel.id)]

                    if 'company_id' in self.env.context:
                        vals.update({'company_id': self.env.context.get('company_id')})

                    if message.wa_message_id:
                        vals.update({'message_id': values.get('wa_message_id')})

                    if self.env.context.get('whatsapp_application'):
                        self.env['whatsapp.history'].sudo().with_context({'whatsapp_application': True,'cron':self.env.context.get(
                                 'cron')}).create(vals)

                    if message.parent_id and not self.env.context.get(
                            'whatsapp_application') and self.env.context.get(
                        'message') != 'received':
                        self.env['whatsapp.history'].sudo().with_context(
                            {'wa_messsage_id': message, 'message_parent_id': message.parent_id,'cron':self.env.context.get(
                                 'cron')}).create(vals)

                    if not message.parent_id and not self.env.context.get(
                            'whatsapp_application') and self.env.context.get(
                        'message') != 'received' and not self.env.context.get('template_send'):
                        self.env['whatsapp.history'].sudo().with_context({'wa_messsage_id': message,'cron':self.env.context.get(
                                 'cron')}).create(vals)
                    if self.env.context.get('template_send'):
                        self.env['whatsapp.history'].sudo().with_context(
                            {'wa_messsage_id': message, 'template_send': True,'cron':self.env.context.get(
                                 'cron'),
                             'wa_template': self.env.context.get(
                                 'wa_template'),
                             'attachment_ids': self.env.context.get(
                                 'attachment_ids'),
                             'active_model_id': self.env.context.get(
                                 'active_model_id')}).create(vals)
        return messages